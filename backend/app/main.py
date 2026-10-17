from fastapi import FastAPI

from app.api.routes.items import router as items_router
from app.api.routes.system import router as system_router
from app.core.config import settings

# Inicializacao da aplicacao FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para Sistemas Distribuidos com persistencia PostgreSQL e SQLAlchemy",
    version=settings.VERSION,
)

# Registro dos roteadores da API
app.include_router(system_router)
app.include_router(items_router)
