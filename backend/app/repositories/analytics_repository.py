"""Repository for anonymous analytics persistence."""

from datetime import UTC, date, datetime, time, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.visitor_event import VisitorEvent


class AnalyticsRepository:
    """CRUD and aggregate queries for visitor events."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        event_type: str,
        page: str | None,
        country_code: str | None,
        session_id_hash: str,
    ) -> VisitorEvent:
        record = VisitorEvent(
            event_type=event_type,
            page=page,
            country_code=country_code,
            session_id_hash=session_id_hash,
        )
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return record

    async def summary(
        self,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> tuple[int, list[tuple[str, int]]]:
        conditions = [VisitorEvent.event_type == "page_view"]
        if start_date:
            conditions.append(
                VisitorEvent.created_at
                >= datetime.combine(start_date, time.min, tzinfo=UTC)
            )
        if end_date:
            conditions.append(
                VisitorEvent.created_at
                < datetime.combine(end_date + timedelta(days=1), time.min, tzinfo=UTC)
            )

        visitor_query = select(
            func.count(func.distinct(VisitorEvent.session_id_hash))
        ).where(*conditions)
        visitor_count = int(
            (await self.session.execute(visitor_query)).scalar_one() or 0
        )

        country_query = (
            select(
                func.coalesce(VisitorEvent.country_code, "??"),
                func.count(func.distinct(VisitorEvent.session_id_hash)),
            )
            .where(*conditions)
            .group_by(VisitorEvent.country_code)
            .order_by(func.count(func.distinct(VisitorEvent.session_id_hash)).desc())
        )
        country_counts = [
            (str(country), int(count))
            for country, count in (await self.session.execute(country_query)).all()
        ]
        return visitor_count, country_counts
