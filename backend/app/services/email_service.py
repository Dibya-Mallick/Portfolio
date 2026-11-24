"""Email notification service."""

import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmailService:
    """Send contact notifications through Resend."""

    async def send_notification(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """Send a notification email."""
        if (
            not settings.EMAIL_PROVIDER_API_KEY
            or not settings.CONTACT_NOTIFICATION_EMAIL
        ):
            logger.info(
                "Email sending skipped (provider key or recipient not configured). "
                "to=%s subject=%s",
                to_email,
                subject,
            )
            return

        payload = {
            "from": settings.EMAIL_FROM_ADDRESS,
            "to": [to_email],
            "subject": subject,
            "text": body,
        }
        headers = {
            "Authorization": f"Bearer {settings.EMAIL_PROVIDER_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.resend.com/emails",
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
            logger.info("Email notification sent to=%s subject=%s", to_email, subject)
        except httpx.HTTPError:
            logger.exception(
                "Email notification failed to=%s subject=%s", to_email, subject
            )
