"""Pydantic schemas for feedback.

TODO: Add schemas matching the Feedback model — e.g. FeedbackCreate, FeedbackResponse.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    """Incoming feedback payload.

    TODO: Add project reference, sentiment fields, etc.
    """

    page: str | None = Field(None, max_length=500)
    rating: int | None = Field(None, ge=1, le=5)
    comment: str | None = Field(None, max_length=2000)


class FeedbackResponse(BaseModel):
    """Feedback record returned to clients."""

    id: UUID
    page: str | None
    rating: int | None
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
