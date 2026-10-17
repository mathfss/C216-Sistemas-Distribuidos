import pytest
from fastapi.testclient import TestClient
from main import app
from services import item_service

@pytest.fixture
def client():
    """Fornece o TestClient para os testes de integracao."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_item_payload():
    """Payload padrao para criacao de item."""
    return {
        "name": "Cluster Worker",
        "description": "No de computacao distribuida",
        "price": 1250.00
    }

@pytest.fixture(autouse=True)
def reset_database():
    """Garante que a base em memoria seja resetada antes de cada teste."""
    item_service.reset_db()
    yield
