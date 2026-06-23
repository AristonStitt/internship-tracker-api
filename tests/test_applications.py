"""
test_applications.py

These tests check the main internship application CRUD routes.

CRUD means:
- Create
- Read
- Update
- Delete

These tests use the real FastAPI app and the real database session.
For now, that is fine for learning.
Later, you can improve this by using a separate test database.
"""

import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import InternshipApplication


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    """
    Clean the internship_applications table before and after each test.

    Why?
    Tests should not depend on data from previous tests.
    Each test should start with a predictable empty database.
    """

    db = SessionLocal()

    try:
        db.query(InternshipApplication).delete()
        db.commit()
    finally:
        db.close()

    yield

    db = SessionLocal()

    try:
        db.query(InternshipApplication).delete()
        db.commit()
    finally:
        db.close()


def test_create_application_returns_created_application():
    payload = {
        "company": "Microsoft",
        "role": "Software Engineering Intern",
        "status": "applied",
        "location": "Remote",
        "application_url": "https://careers.microsoft.com",
        "date_applied": "2026-06-23",
        "notes": "Applied through careers page.",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["company"] == "Microsoft"
    assert data["role"] == "Software Engineering Intern"
    assert data["status"] == "applied"
    assert data["location"] == "Remote"
    assert data["application_url"] == "https://careers.microsoft.com"
    assert data["date_applied"] == "2026-06-23"
    assert data["notes"] == "Applied through careers page."
    assert "created_at" in data
    assert "updated_at" in data


def test_list_applications_returns_created_applications():
    payload = {
        "company": "Google",
        "role": "Backend Engineering Intern",
        "status": "wishlist",
        "location": "Austin, TX",
        "application_url": "https://careers.google.com",
        "date_applied": None,
        "notes": "Need to apply soon.",
    }

    client.post("/applications", json=payload)

    response = client.get("/applications")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Google"
    assert data[0]["role"] == "Backend Engineering Intern"


def test_get_application_by_id_returns_one_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Amazon",
            "role": "Software Development Engineer Intern",
            "status": "applied",
            "location": "Dallas, TX",
            "application_url": "https://amazon.jobs",
            "date_applied": "2026-06-23",
            "notes": "Submitted resume.",
        },
    )

    application_id = create_response.json()["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["company"] == "Amazon"


def test_get_application_by_invalid_id_returns_404():
    response = client.get("/applications/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found."


def test_update_application_changes_status():
    create_response = client.post(
        "/applications",
        json={
            "company": "Meta",
            "role": "Software Engineering Intern",
            "status": "applied",
            "location": "Remote",
            "application_url": "https://careers.meta.com",
            "date_applied": "2026-06-23",
            "notes": "Initial application.",
        },
    )

    application_id = create_response.json()["id"]

    update_response = client.patch(
        f"/applications/{application_id}",
        json={
            "status": "interviewing",
            "notes": "Moved to interview stage.",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == application_id
    assert data["status"] == "interviewing"
    assert data["notes"] == "Moved to interview stage."


def test_delete_application_removes_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Netflix",
            "role": "Backend Intern",
            "status": "wishlist",
            "location": "Remote",
            "application_url": "https://jobs.netflix.com",
            "date_applied": None,
            "notes": "Interesting backend role.",
        },
    )

    application_id = create_response.json()["id"]

    delete_response = client.delete(f"/applications/{application_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/applications/{application_id}")

    assert get_response.status_code == 404


def test_invalid_status_returns_422():
    payload = {
        "company": "Apple",
        "role": "Software Engineering Intern",
        "status": "maybe kinda applied",
        "location": "Cupertino, CA",
        "application_url": "https://jobs.apple.com",
        "date_applied": "2026-06-23",
        "notes": "Invalid status test.",
    }

    response = client.post("/applications", json=payload)

    assert response.status_code == 422