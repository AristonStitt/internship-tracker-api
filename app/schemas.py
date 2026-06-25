"""
schemas.py

Defines API request and response data shapes.
"""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ApplicationStatus(str, Enum):
    wishlist = "wishlist"
    applied = "applied"
    interviewing = "interviewing"
    offer = "offer"
    rejected = "rejected"


class UserCreate(BaseModel):
    """
    Request body for registering a new user.
    """

    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(BaseModel):
    """
    Response body for returning safe user data.

    Notice:
    hashed_password is intentionally not included.
    """

    id: int
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    Response body returned after login.
    """

    access_token: str
    token_type: str


class ApplicationCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=120)
    role: str = Field(..., min_length=1, max_length=120)
    status: ApplicationStatus = ApplicationStatus.wishlist

    location: str | None = Field(default=None, max_length=120)
    application_url: str | None = Field(default=None, max_length=500)
    date_applied: date | None = None
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=120)
    role: str | None = Field(default=None, min_length=1, max_length=120)
    status: ApplicationStatus | None = None

    location: str | None = Field(default=None, max_length=120)
    application_url: str | None = Field(default=None, max_length=500)
    date_applied: date | None = None
    notes: str | None = None


class ApplicationRead(BaseModel):
    id: int
    company: str
    role: str
    status: str
    location: str | None
    application_url: str | None
    date_applied: date | None
    notes: str | None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)