"""Pydantic schemas for privacy-conscious public analytics."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    """Incoming anonymous page-view event."""

    event_type: str = Field("page_view", pattern="^page_view$")
    page: str | None = Field(None, max_length=500)
    session_id: str = Field(..., min_length=16, max_length=128)


class EventResponse(BaseModel):
    """Analytics event returned internally or for future admin use."""

    id: UUID
    event_type: str
    page: str | None
    created_at: datetime
    country_code: str | None

    model_config = {"from_attributes": True}


class CountryCount(BaseModel):
    """Aggregated visitors for one country."""

    country: str
    visitors: int


class AnalyticsSummary(BaseModel):
    """Public aggregate visitor summary."""

    visitor_count: int
    country_counts: list[CountryCount]
