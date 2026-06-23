"""
main.py

This is the entry point of the FastAPI application.
"""

from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import applications


# For now, this creates the database tables automatically.
# Later, in a more professional setup, you would use Alembic migrations instead.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Internship Tracker API",
    description="A backend API for tracking internship and job applications.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """
    Simple route to confirm that the API is running.
    """

    return {"status": "ok"}


app.include_router(applications.router)