"""
test_health.py

This test checks that the API is alive.
It is intentionally simple.

The point is to prove:
1. pytest can run
2. FastAPI app can be imported
3. the /health route works
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}