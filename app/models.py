"""
models.py

This file defines the database tables.

A SQLAlchemy model represents a table in PostgreSQL.
Each object created from this class represents one row in the table.
"""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InternshipApplication(Base):
    """
    Database table for internship/job applications.
    """

    __tablename__ = "internship_applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    company: Mapped[str] = mapped_column(String(120), index=True)
    role: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(30), default="wishlist")

    location: Mapped[str | None] = mapped_column(String(120), nullable=True)
    application_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    date_applied: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )