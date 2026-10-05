from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models.email import Email
from app.models.mailbox import Mailbox
from app.models.user import User
from app.services.gmail_sync import sync_mailbox

router = APIRouter(tags=["emails"])


def _own_mailbox(db: Session, user: User, mailbox_id: int) -> Mailbox:
    mailbox = db.query(Mailbox).filter_by(id=mailbox_id, user_id=user.id).first()
    if mailbox is None:
        raise HTTPException(status_code=404, detail="Mailbox not found")
    return mailbox


@router.get("/mailboxes")
def list_mailboxes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Mailbox).filter_by(user_id=user.id).all()
    return [{"id": m.id, "provider": m.provider, "account": m.provider_account_id, "status": m.status} for m in rows]


@router.post("/mailboxes/{mailbox_id}/sync")
def sync(
    mailbox_id: int,
    limit: int = Query(50, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mailbox = _own_mailbox(db, user, mailbox_id)
    try:
        return {"synced": sync_mailbox(db, mailbox, limit)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mailboxes/{mailbox_id}/emails")
def list_emails(
    mailbox_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _own_mailbox(db, user, mailbox_id)
    rows = (
        db.query(Email)
        .filter_by(mailbox_id=mailbox_id)
        .order_by(Email.received_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": e.id,
            "thread_id": e.provider_thread_id,
            "sender": e.sender,
            "subject": e.subject,
            "snippet": (e.body_text or "")[:200],
            "received_at": e.received_at,
            "is_read": e.is_read,
        }
        for e in rows
    ]


@router.get("/emails/{email_id}")
def get_email(email_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    e = db.get(Email, email_id)
    if e is None:
        raise HTTPException(status_code=404, detail="Email not found")
    _own_mailbox(db, user, e.mailbox_id)
    return {
        "id": e.id, "thread_id": e.provider_thread_id, "sender": e.sender, "recipients": e.recipients,
        "cc": e.cc, "subject": e.subject, "body_text": e.body_text, "body_html": e.body_html,
        "received_at": e.received_at, "is_read": e.is_read,
    }
