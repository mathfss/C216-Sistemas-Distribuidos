from typing import List, Optional
from schemas.item import ItemCreate, ItemUpdate, ItemPatch

# Simula uma tabela de banco de dados em memoria
_items_db = {
    1: {"id": 1, "name": "Servidor Node A", "description": "No do cluster distribuido", "price": 1500.0},
    2: {"id": 2, "name": "Servidor Node B", "description": "No de processamento", "price": 2200.0},
    3: {"id": 3, "name": "Load Balancer", "description": "Distribuidor de carga", "price": 800.0},
}

def list_items(
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
) -> List[dict]:
    items = list(_items_db.values())

    if search:
        items = [i for i in items if search.lower() in i["name"].lower() or (i["description"] and search.lower() in i["description"].lower())]

    if min_price is not None:
        items = [i for i in items if i["price"] >= min_price]

    return items[skip : skip + limit]

def get_item_by_id(item_id: int) -> Optional[dict]:
    return _items_db.get(item_id)

def create_item(item_data: ItemCreate) -> dict:
    new_id = max(_items_db.keys(), default=0) + 1
    new_item = {"id": new_id, **item_data.model_dump()}
    _items_db[new_id] = new_item
    return new_item

def update_item(item_id: int, item_data: ItemUpdate) -> Optional[dict]:
    if item_id not in _items_db:
        return None
    updated = {"id": item_id, **item_data.model_dump()}
    _items_db[item_id] = updated
    return updated

def patch_item(item_id: int, item_data: ItemPatch) -> Optional[dict]:
    if item_id not in _items_db:
        return None
    current = _items_db[item_id]
    update_dict = item_data.model_dump(exclude_unset=True)
    current.update(update_dict)
    _items_db[item_id] = current
    return current

def delete_item(item_id: int) -> bool:
    if item_id in _items_db:
        del _items_db[item_id]
        return True
    return False

def reset_db():
    _items_db.clear()
    _items_db.update({
        1: {"id": 1, "name": "Servidor Node A", "description": "No do cluster distribuido", "price": 1500.0},
        2: {"id": 2, "name": "Servidor Node B", "description": "No de processamento", "price": 2200.0},
        3: {"id": 3, "name": "Load Balancer", "description": "Distribuidor de carga", "price": 800.0},
    })
