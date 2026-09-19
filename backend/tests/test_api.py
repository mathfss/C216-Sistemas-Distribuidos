import pytest

# Teste 1: Rota raiz
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["pratica"] == "Prática 3"

# Teste 2: Rota de healthcheck
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Teste 3: Rota de status do banco de dados
def test_db_status_structure(client):
    response = client.get("/db-status")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "host" in data
    assert "port" in data
    assert "connected" in data

# Teste 4: Listagem de itens cadastrados
def test_list_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) == 3

# Teste 5: Parametrizacao - Busca de itens por IDs validos existentes
@pytest.mark.parametrize("item_id, expected_name", [
    (1, "Servidor Node A"),
    (2, "Servidor Node B"),
    (3, "Load Balancer"),
])
def test_get_item_by_id_parametrized(client, item_id, expected_name):
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == expected_name

# Teste 6: Caso de Erro - 404 (Item nao encontrado)
def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "nao encontrado" in response.json()["detail"]

# Teste 7: Parametrizacao & Caso de Erro - 400 (ID invalido / negativo ou zero)
@pytest.mark.parametrize("invalid_id", [0, -1, -50])
def test_get_item_invalid_id(client, invalid_id):
    response = client.get(f"/items/{invalid_id}")
    assert response.status_code == 400
    assert "positivo" in response.json()["detail"]

# Teste 8: Criacao de novo item usando fixture de payload
def test_create_item_success(client, sample_item_payload):
    response = client.post("/items", json=sample_item_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["name"] == sample_item_payload["name"]
    assert data["price"] == sample_item_payload["price"]

# Teste 9: Caso de Erro - 422 (Validacao Pydantic com preco negativo)
def test_create_item_validation_error(client):
    invalid_payload = {
        "name": "Item Invalido",
        "description": "Teste erro 422",
        "price": -10.0  # Preco deve ser > 0
    }
    response = client.post("/items", json=invalid_payload)
    assert response.status_code == 422
