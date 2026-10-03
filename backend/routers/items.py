from typing import List, Optional
from fastapi import APIRouter, HTTPException, Path, Query, status
from schemas.item import ItemCreate, ItemUpdate, ItemPatch, ItemResponse
from services import item_service

router = APIRouter(prefix="/items", tags=["Itens"])

# 1. GET (com Query Parameters)
@router.get("", response_model=List[ItemResponse])
def list_items(
    search: Optional[str] = Query(None, description="Filtrar por nome ou descricao"),
    min_price: Optional[float] = Query(None, ge=0, description="Filtrar por preco minimo"),
    skip: int = Query(0, ge=0, description="Pular N registros"),
    limit: int = Query(10, ge=1, le=100, description="Limite de registros por pagina")
):
    return item_service.list_items(search=search, min_price=min_price, skip=skip, limit=limit)

# 2. GET por ID (com Path Parameter)
@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int = Path(..., gt=0, description="ID do item a ser consultado")
):
    item = item_service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com ID {item_id} nao encontrado"
        )
    return item

# 3. POST (criacao de novo recurso)
@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate):
    return item_service.create_item(item_data)

# 4. PUT (atualizacao completa de recurso existente)
@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int = Path(..., gt=0, description="ID do item"),
    item_data: ItemUpdate = ...
):
    updated = item_service.update_item(item_id, item_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com ID {item_id} nao encontrado para atualizacao"
        )
    return updated

# 5. PATCH (atualizacao parcial de recurso)
@router.patch("/{item_id}", response_model=ItemResponse)
def patch_item(
    item_id: int = Path(..., gt=0, description="ID do item"),
    item_data: ItemPatch = ...
):
    patched = item_service.patch_item(item_id, item_data)
    if not patched:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com ID {item_id} nao encontrado para modificacao"
        )
    return patched

# 6. DELETE (remocao de recurso)
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int = Path(..., gt=0, description="ID do item a remover")
):
    success = item_service.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com ID {item_id} nao encontrado para remocao"
        )
    return None
