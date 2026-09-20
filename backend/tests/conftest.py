import pytest
from fastapi.testclient import TestClient
from main import app, fake_db

@pytest.fixture
def client():
    """Fixture que fornece um cliente de testes da aplicacao."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_item_payload():
    """Fixture com dados padrao para criacao de item."""
    return {
        "name": "Cluster Worker",
        "description": "No de computacao distribuida",
        "price": 1250.00
    }

@pytest.fixture(autouse=True)
def reset_database():
    """Fixture automatica para garantir o estado inicial dos dados antes de cada teste."""
    initial_state = {
        1: {"id": 1, "name": "Servidor Node A", "description": "No do cluster distribuido", "price": 1500.0},
        2: {"id": 2, "name": "Servidor Node B", "description": "No de processamento", "price": 2200.0},
        3: {"id": 3, "name": "Load Balancer", "description": "Distribuidor de carga", "price": 800.0},
    }
    fake_db.clear()
    fake_db.update(initial_state)
    yield
