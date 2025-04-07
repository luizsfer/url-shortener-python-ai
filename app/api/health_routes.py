from fastapi import APIRouter
from app.core.logging import api_logger

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Endpoint para verificação de saúde da aplicação.
    Retorna 200 OK se a aplicação estiver funcionando corretamente.
    """
    api_logger.info("Health check realizado com sucesso")
    return {"status": "healthy"} 