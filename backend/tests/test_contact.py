"""Tests for the contact endpoint."""


def test_contact_validation_error(client):
    """Missing required fields returns 422."""
    response = client.post("/api/v1/contact", json={})
    assert response.status_code == 422


def test_contact_name_too_long(client):
    """Name exceeding max length returns 422."""
    payload = {
        "name": "A" * 121,
        "email": "test@example.com",
        "message": "Hello!",
    }
    response = client.post("/api/v1/contact", json=payload)
    assert response.status_code == 422


def test_contact_invalid_email(client):
    """Invalid email format returns 422."""
    payload = {
        "name": "Test User",
        "email": "not-an-email",
        "message": "Hello!",
    }
    response = client.post("/api/v1/contact", json=payload)
    assert response.status_code == 422


def test_contact_honeypot_rejection(client):
    """Filled honeypot field returns 422 (bot detected)."""
    payload = {
        "name": "Bot",
        "email": "bot@example.com",
        "message": "Buy stuff!",
        "website": "http://spam.example.com",
    }
    response = client.post("/api/v1/contact", json=payload)
    assert response.status_code == 422
    assert "Invalid submission" in response.json()["detail"]
