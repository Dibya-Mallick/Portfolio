"""Pydantic schemas for the contact form."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    """Incoming contact form payload."""

    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr = Field(..., max_length=254)
    subject: str | None = Field(None, max_length=180)
    message: str = Field(..., min_length=1, max_length=5000)
    honeypot: str = Field("", alias="website")

    model_config = {"populate_by_name": True}


class ContactResponse(BaseModel):
    """Contact record returned to clients."""

    id: UUID
    name: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class ContactSuccess(BaseModel):
    """Success response after submitting a contact form."""

    message: str
    id: UUID
