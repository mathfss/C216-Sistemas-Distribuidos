from sqlalchemy.orm import Session

from app.models.item import Item
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemPatch, ItemUpdate


class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepository(db)

    def list_items(
        self,
        search: str | None = None,
        min_price: float | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Item]:
        return self.repo.get_all(search=search, min_price=min_price, skip=skip, limit=limit)

    def get_item(self, item_id: int) -> Item | None:
        return self.repo.get_by_id(item_id)

    def create_item(self, item_in: ItemCreate) -> Item:
        return self.repo.create(item_in)

    def update_item(self, item_id: int, item_in: ItemUpdate) -> Item | None:
        return self.repo.update(item_id, item_in)

    def patch_item(self, item_id: int, item_in: ItemPatch) -> Item | None:
        return self.repo.patch(item_id, item_in)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)
