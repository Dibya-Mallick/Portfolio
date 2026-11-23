"""Contact form endpoint."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.logging import get_logger
from app.core.rate_limit import contact_rate_limiter
from app.schemas.contact import ContactCreate, ContactSuccess
from app.services.contact_service import ContactService

logger = get_logger(__name__)

router = APIRouter(tags=["contact"])


@router.post(
    "/contact",
    response_model=ContactSuccess,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    request: Request,
    payload: ContactCreate,
    db: AsyncSession = Depends(get_db),
) -> ContactSuccess:
    """Accept a contact form submission.

    Applies rate limiting and honeypot check before persisting.
    """
    # Rate limiting
    await contact_rate_limiter.check(request)

    # Honeypot check — bots tend to fill hidden fields
    if payload.honeypot:
        logger.warning(
            "Honeypot triggered from %s",
            request.client.host if request.client else "unknown",
        )
        # Return a fake success so bots don't retry
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid submission.",
        )

    service = ContactService(db)
    record = await service.create_contact(payload)

    return ContactSuccess(
        message="Thank you for reaching out! I'll get back to you soon.",
        id=record.id,
    )
