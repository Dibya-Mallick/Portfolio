"""Tests for health check endpoints."""


def test_root(client):
    """Root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Portfolio API"
    assert data["version"] == "1.0.0"


def test_health(client):
    """Health endpoint returns healthy status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
