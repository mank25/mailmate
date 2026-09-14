from urllib.parse import urlencode

import httpx

from app.core.config import settings

GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
AUTHORIZATION_URI = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
PROFILE_URI = "https://gmail.googleapis.com/gmail/v1/users/me/profile"


def build_authorization_url(state: str) -> str:
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": GMAIL_READONLY_SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    return f"{AUTHORIZATION_URI}?{urlencode(params)}"


def exchange_code_for_tokens(code: str) -> dict:
    response = httpx.post(
        TOKEN_URI,
        data={
            "code": code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": settings.google_redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    response.raise_for_status()
    return response.json()


def get_gmail_profile(access_token: str) -> dict:
    response = httpx.get(PROFILE_URI, headers={"Authorization": f"Bearer {access_token}"})
    response.raise_for_status()
    return response.json()
