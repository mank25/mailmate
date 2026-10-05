import base64

from app.services.gmail_sync import parse_message

b = lambda s: base64.urlsafe_b64encode(s.encode()).decode().rstrip("=")
msg = {
    "id": "m1", "threadId": "t1", "internalDate": "1700000000000", "labelIds": ["INBOX", "UNREAD"],
    "payload": {
        "headers": [{"name": "From", "value": "A <a@x.com>"}, {"name": "To", "value": "b@x.com, C <c@x.com>"},
                    {"name": "Subject", "value": "Hi"}],
        "mimeType": "multipart/alternative",
        "parts": [{"mimeType": "text/plain", "body": {"data": b("hello")}},
                  {"mimeType": "text/html", "body": {"data": b("<p>hello</p>")}}],
    },
}


def test_parse_message():
    e = parse_message(msg, 1)
    assert e.body_text == "hello" and e.body_html == "<p>hello</p>"
    assert e.recipients == "b@x.com, c@x.com" and e.is_read is False and e.provider_thread_id == "t1"
