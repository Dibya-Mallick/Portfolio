"""Service layer for privacy-conscious analytics."""

import hashlib
import hmac
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics import AnalyticsSummary, CountryCount, EventCreate


class AnalyticsService:
    """Orchestrates anonymous event processing and aggregation."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)

    @staticmethod
    def hash_session_id(session_id: str) -> str:
        return hmac.new(
            settings.SECRET_KEY.encode(), session_id.encode(), hashlib.sha256
        ).hexdigest()

    async def record_page_view(
        self, event: EventCreate, country_code: str | None
    ) -> None:
        await self.repository.create(
            event_type=event.event_type,
            page=event.page,
            country_code=country_code,
            session_id_hash=self.hash_session_id(event.session_id),
        )

    async def summary(
        self,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> AnalyticsSummary:
        visitor_count, country_counts = await self.repository.summary(
            start_date=start_date,
            end_date=end_date,
        )
        return AnalyticsSummary(
            visitor_count=visitor_count,
            country_counts=[
                CountryCount(country=country, visitors=count)
                for country, count in country_counts
            ],
        )
