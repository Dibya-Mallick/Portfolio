"""VisitorEvent SQLAlchemy model."""

import uuid

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VisitorEvent(Base):
    """Analytics events for visitor tracking.

    TODO: Expand with additional columns (referrer, user_agent, geo, etc.)
    """

    __tablename__ = "visitor_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    page: Mapped[str | None] = mapped_column(String(500), nullable=True)
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    session_id_hash: Mapped[str | None] = mapped_column(
        String(128), nullable=True, index=True
    )
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<VisitorEvent id={self.id} type={self.event_type!r}>"
