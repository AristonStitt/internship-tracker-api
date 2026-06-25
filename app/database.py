"""
database.py

Connects the FastAPI app to PostgreSQL and loads app settings.
"""

from collections.abc import Generator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Settings(BaseSettings):
    """
    Loads settings from the .env file.

    DATABASE_URL connects SQLAlchemy to PostgreSQL.
    SECRET_KEY is used to sign JWT access tokens.
    ACCESS_TOKEN_EXPIRE_MINUTES controls how long login tokens last.
    """

    database_url: str
    secret_key: str = "dev-secret-key-change-later"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


engine = create_engine(settings.database_url, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.
    """

    pass


def get_db() -> Generator[Session, None, None]:
    """
    Gives one database session per request.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()