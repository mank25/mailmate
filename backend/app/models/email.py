from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.db import Base


class Email(Base):
    __tablename__ = "emails"
    __table_args__ = (
        UniqueConstraint("mailbox_id", "provider_message_id", name="uq_mailbox_provider_message"),
    )

    id = Column(Integer, primary_key=True)
    mailbox_id = Column(Integer, ForeignKey("mailboxes.id"), nullable=False)
    provider_message_id = Column(String(255), nullable=False)
    provider_thread_id = Column(String(255), nullable=True)
    sender = Column(String(255), nullable=False)
    recipients = Column(Text, nullable=True)
    cc = Column(Text, nullable=True)
    bcc = Column(Text, nullable=True)
    subject = Column(String(998), nullable=True)
    body_text = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    received_at = Column(DateTime, nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    mailbox = relationship("Mailbox", back_populates="emails")
