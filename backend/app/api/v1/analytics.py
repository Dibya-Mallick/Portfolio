"""Public aggregate analytics endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.rate_limit import RateLimiter
from app.schemas.analytics import AnalyticsSummary, EventCreate
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["analytics"])
analytics_rate_limiter = RateLimiter(max_requests=30, window_seconds=60)


def get_country_code(request: Request) -> str | None:
    """Read country from hosting proxy headers without storing a raw IP."""
    for header in ("cf-ipcountry", "x-vercel-ip-country", "x-country-code"):
        value = request.headers.get(header, "").strip().upper()
        if len(value) == 2 and value.isalpha():
            return value
    return None


@router.post("/analytics/events", status_code=status.HTTP_202_ACCEPTED)
async def record_event(
    request: Request,
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    await analytics_rate_limiter.check(request)
    await AnalyticsService(db).record_page_view(event, get_country_code(request))
    return {"status": "accepted"}


@router.get("/analytics/summary", response_model=AnalyticsSummary)
async def analytics_summary(
    start_date: date | None = None,
    end_date: date | None = None,
    db: AsyncSession = Depends(get_db),
) -> AnalyticsSummary:
    if start_date and end_date and end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date must be on or after start_date",
        )
    return await AnalyticsService(db).summary(
        start_date=start_date,
        end_date=end_date,
    )
