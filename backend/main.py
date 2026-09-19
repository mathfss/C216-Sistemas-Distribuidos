import os
import socket
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="C216 - Sistemas Distribuídos",
    version="3.0.0"
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "c216_db")
DB_USER = os.getenv("DB_USER", "postgres")

# Modelo de dados simples para testes de API
class Item(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)

# "Banco de dados" em memória para simulação nos testes
fake_db = {
    1: {"id": 1, "name": "Servidor Node A", "description": "No do cluster distribuido", "price": 1500.0},
    2: {"id": 2, "name": "Servidor Node B", "description": "No de processamento", "price": 2200.0},
    3: {"id": 3, "name": "Load Balancer", "description": "Distribuidor de carga", "price": 800.0},
}

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "disciplina": "C216 - Sistemas Distribuídos",
        "pratica": "Prática 3"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/db-status")
def db_status():
    connected = False
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=2):
            connected = True
    except Exception:
        connected = False

    return {
        "database": "PostgreSQL",
        "host": DB_HOST,
        "port": DB_PORT,
        "database_name": DB_NAME,
        "connected": connected
    }

@app.get("/items")
def list_items():
    return list(fake_db.values())

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do item deve ser um numero positivo"
        )
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com ID {item_id} nao encontrado"
        )
    return fake_db[item_id]

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    new_id = max(fake_db.keys(), default=0) + 1
    item_data = {"id": new_id, **item.model_dump()}
    fake_db[new_id] = item_data
    return item_data
