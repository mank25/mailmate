import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import encrypt_token
from app.db import get_db
from app.deps import get_current_user
from app.models.mailbox import Mailbox
from app.models.user import User
from app.services import google_oauth

router = APIRouter(prefix="/auth/gmail", tags=["gmail"])

OAUTH_STATE_COOKIE_NAME = "oauth_state"
OAUTH_STATE_MAX_AGE_SECONDS = 600


@router.get("/connect")
def connect(response: Response, current_user: User = Depends(get_current_user)):
    state = secrets.token_urlsafe(32)

    redirect = RedirectResponse(url=google_oauth.build_authorization_url(state))
    redirect.set_cookie(
        key=OAUTH_STATE_COOKIE_NAME,
        value=state,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=OAUTH_STATE_MAX_AGE_SECONDS,
    )
    return redirect


@router.get("/callback")
def callback(
    request: Request,
    code: str,
    state: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cookie_state = request.cookies.get(OAUTH_STATE_COOKIE_NAME)
    if not cookie_state or cookie_state != state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OAuth state")

    tokens = google_oauth.exchange_code_for_tokens(code)
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to obtain access token")

    profile = google_oauth.get_gmail_profile(access_token)
    email_address = profile.get("emailAddress")
    if not email_address:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to identify Gmail account")

    mailbox = (
        db.query(Mailbox)
        .filter(
            Mailbox.user_id == current_user.id,
            Mailbox.provider == "gmail",
            Mailbox.provider_account_id == email_address,
        )
        .first()
    )
    if mailbox is None:
        mailbox = Mailbox(user_id=current_user.id, provider="gmail", provider_account_id=email_address)
        db.add(mailbox)

    mailbox.encrypted_access_token = encrypt_token(access_token)
    if refresh_token:
        mailbox.encrypted_refresh_token = encrypt_token(refresh_token)
    mailbox.status = "connected"
    db.commit()

    redirect = RedirectResponse(url=f"{settings.frontend_url}/dashboard?gmail=connected")
    redirect.delete_cookie(OAUTH_STATE_COOKIE_NAME)
    return redirect
