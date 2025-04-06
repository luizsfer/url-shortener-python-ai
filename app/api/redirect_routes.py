from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.services.url_service import URLService
from app.core.logging import api_logger

router = APIRouter()
url_service = URLService()

@router.get("/{short_code}")
async def redirect_url(request: Request, short_code: str):
    """
    Redireciona para a URL original a partir do código curto.
    """
    try:
        api_logger.info(f"Recebida requisição para redirecionar URL: {short_code}")
        
        # Busca a URL
        url = url_service.get_url(short_code)
        
        if not url:
            api_logger.warning(f"URL não encontrada: {short_code}")
            raise HTTPException(status_code=404, detail="URL não encontrada")
        
        api_logger.info(f"URL encontrada: {short_code} -> {url}")
        return RedirectResponse(url=url, status_code=307)
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Erro ao redirecionar URL: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 