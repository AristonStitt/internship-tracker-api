"""
main.py

Entry point of the FastAPI application.
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import applications, auth


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Internship Tracker API",
    description="A backend API for tracking internship and job applications.",
    version="0.2.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(applications.router)