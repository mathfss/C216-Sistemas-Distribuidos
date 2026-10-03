from fastapi import FastAPI
from routers.items import router as items_router
from routers.system import router as system_router

# Inicializacao da aplicacao FastAPI
app = FastAPI(
    title="C216 - Sistemas Distribuídos",
    description="API com arquitetura modular para a Prática 4",
    version="4.0.0"
)

# Registro dos roteadores modulares
app.include_router(system_router)
app.include_router(items_router)
