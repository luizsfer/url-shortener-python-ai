from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.security.memory_security import MemorySecurity
from app.core.logging import security_logger

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.security = MemorySecurity()
        security_logger.info("Middleware de segurança inicializado")
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Obtém o IP do cliente
            client_ip = request.client.host if request.client else "unknown"
            
            # Ignora o rate limit para requisições de redirecionamento
            if not request.url.path.startswith("/api/"):
                # Processa a requisição
                response = await call_next(request)
                return response
            
            # Verifica o limite de requisições
            if not self.security.check_rate_limit(client_ip):
                security_logger.warning(f"Requisição bloqueada de IP: {client_ip}")
                raise HTTPException(status_code=429, detail="Muitas requisições")
            
            # Processa a requisição
            response = await call_next(request)
            
            # Se a resposta indicar erro, registra a falha
            if response.status_code >= 400:
                self.security.record_failed_request(client_ip)
            
            return response
        except HTTPException:
            raise
        except Exception as e:
            security_logger.error(f"Erro no middleware de segurança: {e}")
            raise HTTPException(status_code=500, detail="Erro interno do servidor")