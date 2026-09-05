import os
import socket
from fastapi import FastAPI

app = FastAPI(
    title="C216 - Sistemas Distribuídos",
    description="API para o Ambiente Distribuído com Docker Compose (Prática 2)",
    version="2.0.0"
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "c216_db")
DB_USER = os.getenv("DB_USER", "postgres")

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "disciplina": "C216 - Sistemas Distribuídos",
        "pratica": "Prática 2 - Docker & Docker Compose",
        "mensagem": "Serviço backend rodando em container e integrado com Docker Compose!"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/db-status")
def db_status():
    """Verifica a conectividade de rede com o serviço de banco de dados do Docker Compose."""
    is_connected = False
    details = ""
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=2):
            is_connected = True
            details = f"Conexão TCP estabelecida com sucesso com {DB_HOST}:{DB_PORT}"
    except Exception as e:
        details = f"Falha na conexão com {DB_HOST}:{DB_PORT} - Erro: {str(e)}"

    return {
        "database": "PostgreSQL",
        "host": DB_HOST,
        "port": DB_PORT,
        "database_name": DB_NAME,
        "connected": is_connected,
        "details": details
    }
