"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture()
def client():
    """Synchronous test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture()
async def async_client():
    """Async test client using httpx."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
