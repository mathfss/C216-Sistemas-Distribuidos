from typing import Optional
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do item")
    description: Optional[str] = Field(None, description="Descricao do item")
    price: float = Field(..., gt=0, description="Preco deve ser maior que zero")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)

class ItemResponse(ItemBase):
    id: int
