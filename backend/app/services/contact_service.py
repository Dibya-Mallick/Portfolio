"""Service layer for contact form submissions."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.models.contact import ContactMessage
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate
from app.services.email_service import EmailService

logger = get_logger(__name__)


class ContactService:
    """Orchestrates contact form processing."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = ContactRepository(session)
        self.email = EmailService()

    async def create_contact(self, data: ContactCreate) -> ContactMessage:
        """Validate, persist, and optionally notify on a new contact message."""
        record = await self.repo.create(data)
        logger.info("Contact message created id=%s from=%s", record.id, record.email)

        # Fire-and-forget notification (best-effort)
        if settings.CONTACT_NOTIFICATION_EMAIL:
            await self.email.send_notification(
                to_email=settings.CONTACT_NOTIFICATION_EMAIL,
                subject=f"New contact from {record.name}",
                body=f"{record.name} ({record.email}): {record.message[:200]}",
            )

        return record
