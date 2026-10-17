from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do item")
    description: str | None = Field(None, description="Descricao do item")
    price: float = Field(..., gt=0, description="Preco deve ser maior que zero")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemPatch(BaseModel):
    name: str | None = Field(None, min_length=1)
    description: str | None = None
    price: float | None = Field(None, gt=0)


class ItemResponse(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
