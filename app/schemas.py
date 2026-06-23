"""
schemas.py

This file defines the data shapes for API input and output.

FastAPI uses Pydantic schemas to validate incoming JSON and format outgoing JSON.
"""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ApplicationStatus(str, Enum):
    """
    Allowed status values for an application.

    Using an Enum prevents random invalid statuses like:
    - "kinda applied"
    - "maybe"
    - "waiting lol"
    """

    wishlist = "wishlist"
    applied = "applied"
    interviewing = "interviewing"
    offer = "offer"
    rejected = "rejected"


class ApplicationCreate(BaseModel):
    """
    Schema for creating a new internship application.

    This controls what the client is allowed to send in a POST request.
    """

    company: str = Field(..., min_length=1, max_length=120)
    role: str = Field(..., min_length=1, max_length=120)
    status: ApplicationStatus = ApplicationStatus.wishlist

    location: str | None = Field(default=None, max_length=120)
    application_url: str | None = Field(default=None, max_length=500)
    date_applied: date | None = None
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    """
    Schema for updating an application.

    Every field is optional because PATCH requests usually update only part of a resource.
    """

    company: str | None = Field(default=None, min_length=1, max_length=120)
    role: str | None = Field(default=None, min_length=1, max_length=120)
    status: ApplicationStatus | None = None

    location: str | None = Field(default=None, max_length=120)
    application_url: str | None = Field(default=None, max_length=500)
    date_applied: date | None = None
    notes: str | None = None


class ApplicationRead(BaseModel):
    """
    Schema for returning application data to the client.

    This includes database-generated fields like id, created_at, and updated_at.
    """

    id: int
    company: str
    role: str
    status: str
    location: str | None
    application_url: str | None
    date_applied: date | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)