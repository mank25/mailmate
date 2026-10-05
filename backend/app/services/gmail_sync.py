import base64
from datetime import datetime, timezone
from email.utils import getaddresses

import httpx
from sqlalchemy.orm import Session

from app.core.security import decrypt_token
from app.models.email import Email
from app.models.mailbox import Mailbox
from app.services import google_oauth

API = "https://gmail.googleapis.com/gmail/v1/users/me"


def _get(access_token: str, path: str, **params) -> dict:
    r = httpx.get(f"{API}/{path}", params=params, headers={"Authorization": f"Bearer {access_token}"})
    r.raise_for_status()
    return r.json()


def _decode(data: str) -> str:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")


def _bodies(part: dict, out: dict) -> None:
    mime, data = part.get("mimeType"), part.get("body", {}).get("data")
    if data and mime in ("text/plain", "text/html"):
        out.setdefault(mime, _decode(data))
    for sub in part.get("parts", []):
        _bodies(sub, out)


def parse_message(msg: dict, mailbox_id: int) -> Email:
    headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
    bodies: dict = {}
    _bodies(msg["payload"], bodies)
    addrs = lambda k: ", ".join(a for _, a in getaddresses([headers.get(k, "")]) if a) or None
    return Email(
        mailbox_id=mailbox_id,
        provider_message_id=msg["id"],
        provider_thread_id=msg.get("threadId"),
        sender=headers.get("from", "")[:255],
        recipients=addrs("to"),
        cc=addrs("cc"),
        bcc=addrs("bcc"),
        subject=headers.get("subject"),
        body_text=bodies.get("text/plain"),
        body_html=bodies.get("text/html"),
        received_at=datetime.fromtimestamp(int(msg["internalDate"]) / 1000, timezone.utc).replace(tzinfo=None),
        is_read="UNREAD" not in msg.get("labelIds", []),
    )


def sync_mailbox(db: Session, mailbox: Mailbox, limit: int = 50) -> int:
    """Fetch the newest `limit` INBOX messages we don't have yet. Returns number stored."""
    refresh = decrypt_token(mailbox.encrypted_refresh_token or "")
    if not refresh:
        mailbox.status = "error"
        db.commit()
        raise ValueError("Mailbox has no usable refresh token; reconnect Gmail")
    token = google_oauth.refresh_access_token(refresh)

    ids: list[str] = []
    page = None
    while len(ids) < limit:
        params = {"labelIds": "INBOX", "maxResults": min(limit - len(ids), 100)}
        if page:
            params["pageToken"] = page
        res = _get(token, "messages", **params)
        ids += [m["id"] for m in res.get("messages", [])]
        page = res.get("nextPageToken")
        if not page:
            break

    known = {
        i for (i,) in db.query(Email.provider_message_id).filter(
            Email.mailbox_id == mailbox.id, Email.provider_message_id.in_(ids)
        )
    }
    new = [i for i in ids if i not in known]
    # ponytail: sequential fetch, move to the queue / batch API for large inboxes
    for mid in new:
        db.add(parse_message(_get(token, f"messages/{mid}", format="full"), mailbox.id))
    db.commit()
    return len(new)
