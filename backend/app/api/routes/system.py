from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import get_db

router = APIRouter(tags=["Sistema"])


@router.get("/")
def read_root():
    return {
        "status": "ok",
        "disciplina": "C216 - Sistemas Distribuídos",
        "pratica": "Prática 5 - Persistência com PostgreSQL, SQLAlchemy & Migrations",
    }


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/db-status")
def db_status(db: Session = Depends(get_db)):
    connected = False
    details = ""
    try:
        db.execute(text("SELECT 1"))
        connected = True
        details = "Conexao com banco de dados estabelecida com sucesso"
    except Exception as e:
        connected = False
        details = f"Falha na conexao: {e!s}"

    return {
        "database": "PostgreSQL",
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database_name": settings.DB_NAME,
        "connected": connected,
        "details": details,
    }
