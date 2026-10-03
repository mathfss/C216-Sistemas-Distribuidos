import pytest

# 1. GET /items (com e sem Query Parameters)
def test_list_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

def test_list_items_with_query_params(client):
    response = client.get("/items?search=Node&min_price=2000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Servidor Node B"

def test_list_items_pagination_query_params(client):
    response = client.get("/items?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 2

# 2. GET /items/{item_id} (Path Parameter)
@pytest.mark.parametrize("item_id, expected_name", [
    (1, "Servidor Node A"),
    (2, "Servidor Node B"),
    (3, "Load Balancer"),
])
def test_get_item_by_id_success(client, item_id, expected_name):
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == expected_name

def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "nao encontrado" in response.json()["detail"]

def test_get_item_invalid_path_param(client):
    response = client.get("/items/0")
    assert response.status_code == 422  # gt=0 no Path param

# 3. POST /items
def test_create_item_success(client, sample_item_payload):
    response = client.post("/items", json=sample_item_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["name"] == sample_item_payload["name"]
    assert data["price"] == sample_item_payload["price"]

def test_create_item_validation_error(client):
    payload = {"name": "", "price": -50.0}
    response = client.post("/items", json=payload)
    assert response.status_code == 422

# 4. PUT /items/{item_id}
def test_update_item_success(client):
    update_data = {
        "name": "Servidor Node A (Cluster Pro)",
        "description": "Atualizacao completa",
        "price": 2500.0
    }
    response = client.put("/items/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == update_data["name"]
    assert data["price"] == 2500.0

def test_update_item_not_found(client):
    update_data = {"name": "Item X", "description": "Teste", "price": 100.0}
    response = client.put("/items/999", json=update_data)
    assert response.status_code == 404

# 5. PATCH /items/{item_id}
def test_patch_item_partial(client):
    patch_data = {"price": 1750.50}
    response = client.patch("/items/1", json=patch_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Servidor Node A"
    assert data["price"] == 1750.50

def test_patch_item_not_found(client):
    response = client.patch("/items/999", json={"price": 500.0})
    assert response.status_code == 404

# 6. DELETE /items/{item_id}
def test_delete_item_success_and_verify(client):
    response = client.delete("/items/1")
    assert response.status_code == 204

    # Confirma que foi deletado
    get_res = client.get("/items/1")
    assert get_res.status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
