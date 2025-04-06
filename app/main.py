from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.url_routes import router as url_router
from app.api.redirect_routes import router as redirect_router
from app.core.config import get_settings
from app.security.middleware import SecurityMiddleware
from app.core.logging import api_logger
import os

settings = get_settings()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adiciona o middleware de segurança
app.add_middleware(SecurityMiddleware)

# Registra as rotas
app.include_router(redirect_router, prefix="", tags=["redirect"])
app.include_router(url_router, prefix="/api/v1", tags=["urls"])

@app.on_event("startup")
async def startup_event():
    api_logger.info("API iniciada com sucesso")
    api_logger.info(f"Host: 0.0.0.0")
    api_logger.info(f"Port: {os.getenv('PORT', '8000')}")

@app.on_event("shutdown")
async def shutdown_event():
    api_logger.info("API encerrada com sucesso") 