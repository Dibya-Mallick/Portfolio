"""ContactMessage SQLAlchemy model."""

import uuid

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ContactMessage(Base):
    """Persisted contact form submissions."""

    __tablename__ = "contact_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(180), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    status: Mapped[str] = mapped_column(String(20), default="new", server_default="new")
    source_page: Mapped[str | None] = mapped_column(String(200), nullable=True)

    def __repr__(self) -> str:
        return f"<ContactMessage id={self.id} name={self.name!r}>"
