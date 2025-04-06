from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional
from app.services.url_service import URLService
from app.schemas.url import URLInput, URLResponse, URLStats, URLList, URLUpdate
from app.core.logging import api_logger
from app.security.memory_security import MemorySecurity

router = APIRouter()
url_service = URLService()
security = MemorySecurity()

@router.get("/health")
async def health_check(request: Request):
    """
    Verifica a saúde da API.
    """
    try:
        api_logger.info("Recebida requisição para verificar saúde da API")
        
        # Verifica a saúde do repositório
        is_healthy = url_service.health_check()
        
        if not is_healthy:
            api_logger.error("Falha ao verificar saúde da API")
            raise HTTPException(status_code=503, detail="Serviço indisponível")
        
        api_logger.info("Verificação de saúde da API concluída com sucesso")
        return {"status": "healthy"}
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Erro ao verificar saúde da API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/shorten", response_model=URLResponse)
async def shorten_url(request: Request, url_input: URLInput):
    """
    Encurta uma URL.
    """
    try:
        api_logger.info(f"Recebida requisição para encurtar URL: {url_input.url}")
        
        # Valida e sanitiza a URL
        if not security.validate_url(url_input.url):
            api_logger.warning(f"URL inválida: {url_input.url}")
            raise HTTPException(status_code=400, detail="URL inválida")
        
        url = security.sanitize_url(url_input.url)
        
        # Encurta a URL
        short_code = url_service.shorten_url(url)
        
        api_logger.info(f"URL encurtada com sucesso: {short_code}")
        return URLResponse(short_code=short_code, original_url=url)
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Erro ao encurtar URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/urls", response_model=URLList)
async def list_urls(
    request: Request,
    skip: int = Query(0, ge=0, description="Número de URLs para pular"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de URLs para retornar")
):
    """
    Lista URLs com paginação.
    """
    try:
        api_logger.info(f"Recebida requisição para listar URLs (skip={skip}, limit={limit})")
        
        # Lista as URLs
        urls = url_service.list_urls(skip, limit)
        total = url_service.count_urls()
        
        api_logger.info(f"Listagem de URLs obtida com sucesso: {len(urls)} URLs")
        return URLList(urls=urls, total=total)
    except Exception as e:
        api_logger.error(f"Erro ao listar URLs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/{short_code}", response_model=URLStats)
async def get_url_stats(request: Request, short_code: str):
    """
    Obtém estatísticas de uma URL.
    """
    try:
        api_logger.info(f"Recebida requisição para obter estatísticas: {short_code}")
        
        # Busca as estatísticas
        stats = url_service.get_url_stats(short_code)
        
        if not stats:
            api_logger.warning(f"Estatísticas não encontradas: {short_code}")
            raise HTTPException(status_code=404, detail="URL não encontrada")
        
        api_logger.info(f"Estatísticas obtidas com sucesso: {short_code}")
        return URLStats(**stats)
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{short_code}")
async def delete_url(request: Request, short_code: str):
    """
    Exclui uma URL.
    """
    try:
        api_logger.info(f"Recebida requisição para excluir URL: {short_code}")
        
        # Exclui a URL
        success = url_service.delete_url(short_code)
        
        if not success:
            api_logger.warning(f"URL não encontrada para exclusão: {short_code}")
            raise HTTPException(status_code=404, detail="URL não encontrada")
        
        api_logger.info(f"URL excluída com sucesso: {short_code}")
        return {"message": "URL excluída com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Erro ao excluir URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{short_code}", response_model=URLResponse)
async def update_url(request: Request, short_code: str, url_update: URLUpdate):
    """
    Atualiza uma URL.
    """
    try:
        api_logger.info(f"Recebida requisição para atualizar URL: {short_code}")
        
        # Valida e sanitiza a URL
        if not security.validate_url(url_update.url):
            api_logger.warning(f"URL inválida para atualização: {url_update.url}")
            raise HTTPException(status_code=400, detail="URL inválida")
        
        url = security.sanitize_url(url_update.url)
        
        # Atualiza a URL
        success = url_service.update_url(short_code, url)
        
        if not success:
            api_logger.warning(f"URL não encontrada para atualização: {short_code}")
            raise HTTPException(status_code=404, detail="URL não encontrada")
        
        api_logger.info(f"URL atualizada com sucesso: {short_code}")
        return URLResponse(short_code=short_code, original_url=url)
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Erro ao atualizar URL: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 