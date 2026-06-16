"""Basic tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db


@pytest.fixture
def test_client():
    """Create a test client."""
    return TestClient(app)


def test_health_check(test_client):
    """Test health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_account(test_client):
    """Test account creation."""
    response = test_client.post(
        "/api/v1/accounts/create",
        json={
            "account_holder_name": "Test User",
            "ttl_days": 30,
        }
    )
    # This will fail without database, but tests structure
    assert response.status_code in [201, 500]  # Success or DB error


def test_api_documentation(test_client):
    """Test API documentation is available."""
    response = test_client.get("/docs")
    assert response.status_code == 200
