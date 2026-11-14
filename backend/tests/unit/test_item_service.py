from app.schemas.item import ItemCreate, ItemPatch, ItemUpdate
from app.services.item_service import ItemService


def test_list_items_default(db_session):
    service = ItemService(db_session)
    items = service.list_items()
    assert len(items) == 3


def test_list_items_search_filter(db_session):
    service = ItemService(db_session)
    results = service.list_items(search="Balancer")
    assert len(results) == 1
    assert results[0].name == "Load Balancer"


def test_list_items_min_price_filter(db_session):
    service = ItemService(db_session)
    results = service.list_items(min_price=2000.0)
    assert len(results) == 1
    assert results[0].name == "Servidor Node B"


def test_get_item_by_id_exists(db_session):
    service = ItemService(db_session)
    item = service.get_item(1)
    assert item is not None
    assert item.name == "Servidor Node A"


def test_get_item_by_id_not_found(db_session):
    service = ItemService(db_session)
    item = service.get_item(999)
    assert item is None


def test_create_item(db_session):
    service = ItemService(db_session)
    payload = ItemCreate(name="Gateway API", description="Ponto de entrada", price=1100.0)
    created = service.create_item(payload)
    assert created.id == 4
    assert created.name == "Gateway API"


def test_update_item_success(db_session):
    service = ItemService(db_session)
    payload = ItemUpdate(name="Node A Atualizado", description="Nova descricao", price=1800.0)
    updated = service.update_item(1, payload)
    assert updated is not None
    assert updated.name == "Node A Atualizado"
    assert updated.price == 1800.0


def test_update_item_not_found(db_session):
    service = ItemService(db_session)
    payload = ItemUpdate(name="Inexistente", description="Desc", price=100.0)
    updated = service.update_item(999, payload)
    assert updated is None


def test_patch_item_partial(db_session):
    service = ItemService(db_session)
    patch_payload = ItemPatch(price=1999.0)
    patched = service.patch_item(1, patch_payload)
    assert patched is not None
    assert patched.price == 1999.0
    assert patched.name == "Servidor Node A"


def test_delete_item_success_and_not_found(db_session):
    service = ItemService(db_session)
    assert service.delete_item(1) is True
    assert service.get_item(1) is None
    assert service.delete_item(1) is False
