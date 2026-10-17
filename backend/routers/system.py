import os
import socket
from fastapi import APIRouter

router = APIRouter(tags=["Sistema"])

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "c216_db")

@router.get("/")
def read_root():
    return {
        "status": "ok",
        "disciplina": "C216 - Sistemas Distribuídos",
        "pratica": "Prática 4 - Arquiteturas & APIs com FastAPI"
    }

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/db-status")
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
