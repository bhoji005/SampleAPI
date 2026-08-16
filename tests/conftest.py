import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import store


@pytest.fixture
def client() -> TestClient:
    store.clear()
    with TestClient(app) as test_client:
        yield test_client
    store.clear()


@pytest.fixture
def sample_payload() -> dict:
    return {
        "name": "Widget",
        "description": "A useful widget",
        "price": 9.99,
        "quantity": 3,
    }
