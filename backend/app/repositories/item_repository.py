from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemPatch, ItemUpdate


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        search: str | None = None,
        min_price: float | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Item]:
        query = select(Item)
        if search:
            search_pattern = f"%{search.lower()}%"
            query = query.where(
                Item.name.ilike(search_pattern) | Item.description.ilike(search_pattern)
            )
        if min_price is not None:
            query = query.where(Item.price >= min_price)
        query = query.offset(skip).limit(limit)
        return list(self.db.scalars(query).all())

    def get_by_id(self, item_id: int) -> Item | None:
        return self.db.get(Item, item_id)

    def create(self, item_in: ItemCreate) -> Item:
        db_item = Item(
            name=item_in.name,
            description=item_in.description,
            price=item_in.price,
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, item_id: int, item_in: ItemUpdate) -> Item | None:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        db_item.name = item_in.name
        db_item.description = item_in.description
        db_item.price = item_in.price
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def patch(self, item_id: int, item_in: ItemPatch) -> Item | None:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None
        update_data = item_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: int) -> bool:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return False
        self.db.delete(db_item)
        self.db.commit()
        return True
