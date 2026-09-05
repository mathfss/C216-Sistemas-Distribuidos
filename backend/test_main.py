from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "mensagem" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_db_status_endpoint_structure():
    response = client.get("/db-status")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "host" in data
    assert "port" in data
    assert "connected" in data
