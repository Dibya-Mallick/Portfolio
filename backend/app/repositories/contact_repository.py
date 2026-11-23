"""Repository for contact message persistence."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactMessage
from app.schemas.contact import ContactCreate


class ContactRepository:
    """CRUD operations for ContactMessage."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: ContactCreate) -> ContactMessage:
        """Insert a new contact message and return the persisted record."""
        record = ContactMessage(
            name=data.name,
            email=data.email,
            subject=data.subject,
            message=data.message,
        )
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return record
