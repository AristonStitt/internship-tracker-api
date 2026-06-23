"""
database.py

This file is responsible for connecting the FastAPI app to PostgreSQL.

Important idea:
- FastAPI handles HTTP requests.
- PostgreSQL stores the data.
- SQLAlchemy is the bridge between Python code and the database.
"""

from collections.abc import Generator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Settings(BaseSettings):
    """
    Loads environment variables from the .env file.

    database_url will come from:
    DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/internship_tracker
    """

    database_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


# The engine is the main connection point to the database.
engine = create_engine(settings.database_url, echo=True)


# SessionLocal creates database sessions.
# A session is like a temporary workspace for talking to the database.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy database models.

    Every database table class will inherit from this.
    """

    pass


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that gives one database session per request.

    The request gets a database session.
    When the request is finished, the session closes.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()