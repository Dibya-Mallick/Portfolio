"""Feedback SQLAlchemy model."""

import uuid

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Feedback(Base):
    """User feedback on portfolio projects or content.

    TODO: Expand with project reference, sentiment analysis, etc.
    """

    __tablename__ = "feedback"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    page: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<Feedback id={self.id} rating={self.rating}>"
