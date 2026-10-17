import pytest
from schemas.item import ItemCreate, ItemUpdate, ItemPatch
from services import item_service

def test_list_items_default():
    items = item_service.list_items()
    assert len(items) == 3

def test_list_items_search_filter():
    results = item_service.list_items(search="Balancer")
    assert len(results) == 1
    assert results[0]["name"] == "Load Balancer"

def test_list_items_min_price_filter():
    results = item_service.list_items(min_price=2000.0)
    assert len(results) == 1
    assert results[0]["name"] == "Servidor Node B"

def test_get_item_by_id_exists():
    item = item_service.get_item_by_id(1)
    assert item is not None
    assert item["name"] == "Servidor Node A"

def test_get_item_by_id_not_found():
    item = item_service.get_item_by_id(999)
    assert item is None

def test_create_item():
    payload = ItemCreate(name="Gateway API", description="Ponto de entrada", price=1100.0)
    created = item_service.create_item(payload)
    assert created["id"] == 4
    assert created["name"] == "Gateway API"

def test_update_item_success():
    payload = ItemUpdate(name="Node A Atualizado", description="Nova descricao", price=1800.0)
    updated = item_service.update_item(1, payload)
    assert updated is not None
    assert updated["name"] == "Node A Atualizado"
    assert updated["price"] == 1800.0

def test_update_item_not_found():
    payload = ItemUpdate(name="Inexistente", description="Desc", price=100.0)
    updated = item_service.update_item(999, payload)
    assert updated is None

def test_patch_item_partial():
    # Atualiza apenas o preco mantendo o nome
    patch_payload = ItemPatch(price=1999.0)
    patched = item_service.patch_item(1, patch_payload)
    assert patched is not None
    assert patched["price"] == 1999.0
    assert patched["name"] == "Servidor Node A"

def test_delete_item_success_and_not_found():
    assert item_service.delete_item(1) is True
    assert item_service.get_item_by_id(1) is None
    assert item_service.delete_item(1) is False
