from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.items import router as items_router
from app.api.routes.system import router as system_router
from app.core.config import settings

# Inicializacao da aplicacao FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para Sistemas Distribuidos com persistencia PostgreSQL e SQLAlchemy",
    version=settings.VERSION,
)

# Configuracao de CORS com origens explicitas
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Registro dos roteadores da API
app.include_router(system_router)
app.include_router(items_router)
