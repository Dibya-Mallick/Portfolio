"""Email notification service."""

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmailService:
    """Send email notifications.

    Currently logs instead of sending. Swap in a real provider
    (SendGrid, SES, Resend, etc.) when EMAIL_PROVIDER_API_KEY is set.
    """

    async def send_notification(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """Send a notification email."""
        if not settings.EMAIL_PROVIDER_API_KEY:
            logger.info(
                "Email sending skipped (no provider key). to=%s subject=%s",
                to_email,
                subject,
            )
            return

        # TODO: Integrate with email provider API
        logger.info("Sending email to=%s subject=%s", to_email, subject)
