"""
test_applications.py

Tests for authenticated application CRUD.
"""

import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import InternshipApplication, User


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    """
    Clean tables before and after each test.

    Delete applications first because applications depend on users.
    """

    db = SessionLocal()

    try:
        db.query(InternshipApplication).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

    yield

    db = SessionLocal()

    try:
        db.query(InternshipApplication).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


def auth_headers(email: str = "test@example.com", password: str = "password123") -> dict:
    """
    Register and log in a user.

    Returns the Authorization header needed for protected routes.
    """

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_create_application_requires_authentication():
    response = client.post(
        "/applications",
        json={
            "company": "Microsoft",
            "role": "Software Engineering Intern",
            "status": "applied",
        },
    )

    assert response.status_code == 401


def test_create_application_returns_created_application_for_current_user():
    headers = auth_headers()

    payload = {
        "company": "Microsoft",
        "role": "Software Engineering Intern",
        "status": "applied",
        "location": "Remote",
        "application_url": "https://careers.microsoft.com",
        "date_applied": "2026-06-23",
        "notes": "Applied through careers page.",
    }

    response = client.post("/applications", json=payload, headers=headers)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["company"] == "Microsoft"
    assert data["role"] == "Software Engineering Intern"
    assert data["status"] == "applied"
    assert data["owner_id"] is not None


def test_list_applications_returns_only_current_users_applications():
    user_one_headers = auth_headers("one@example.com", "password123")
    user_two_headers = auth_headers("two@example.com", "password123")

    client.post(
        "/applications",
        json={
            "company": "Google",
            "role": "Backend Intern",
            "status": "applied",
        },
        headers=user_one_headers,
    )

    client.post(
        "/applications",
        json={
            "company": "Amazon",
            "role": "SDE Intern",
            "status": "applied",
        },
        headers=user_two_headers,
    )

    response = client.get("/applications", headers=user_one_headers)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Google"


def test_get_application_by_id_returns_owned_application():
    headers = auth_headers()

    create_response = client.post(
        "/applications",
        json={
            "company": "Amazon",
            "role": "Software Development Engineer Intern",
            "status": "applied",
        },
        headers=headers,
    )

    application_id = create_response.json()["id"]

    response = client.get(f"/applications/{application_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["company"] == "Amazon"


def test_user_cannot_get_another_users_application():
    user_one_headers = auth_headers("one@example.com", "password123")
    user_two_headers = auth_headers("two@example.com", "password123")

    create_response = client.post(
        "/applications",
        json={
            "company": "Meta",
            "role": "Software Engineering Intern",
            "status": "applied",
        },
        headers=user_one_headers,
    )

    application_id = create_response.json()["id"]

    response = client.get(f"/applications/{application_id}", headers=user_two_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found."


def test_update_application_changes_status():
    headers = auth_headers()

    create_response = client.post(
        "/applications",
        json={
            "company": "Meta",
            "role": "Software Engineering Intern",
            "status": "applied",
        },
        headers=headers,
    )

    application_id = create_response.json()["id"]

    update_response = client.patch(
        f"/applications/{application_id}",
        json={
            "status": "interviewing",
            "notes": "Moved to interview stage.",
        },
        headers=headers,
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == application_id
    assert data["status"] == "interviewing"
    assert data["notes"] == "Moved to interview stage."


def test_delete_application_removes_application():
    headers = auth_headers()

    create_response = client.post(
        "/applications",
        json={
            "company": "Netflix",
            "role": "Backend Intern",
            "status": "wishlist",
        },
        headers=headers,
    )

    application_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/applications/{application_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/applications/{application_id}",
        headers=headers,
    )

    assert get_response.status_code == 404


def test_invalid_status_returns_422():
    headers = auth_headers()

    payload = {
        "company": "Apple",
        "role": "Software Engineering Intern",
        "status": "maybe kinda applied",
    }

    response = client.post("/applications", json=payload, headers=headers)

    assert response.status_code == 422