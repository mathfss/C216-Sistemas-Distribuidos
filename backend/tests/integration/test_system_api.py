def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Prática 4" in data["pratica"]

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_db_status_endpoint(client):
    response = client.get("/db-status")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "host" in data
    assert "connected" in data
