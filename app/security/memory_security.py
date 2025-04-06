from datetime import datetime, timedelta
from typing import Dict, Set
from urllib.parse import urlparse
from app.core.config import get_settings
from app.core.logging import security_logger

settings = get_settings()

class MemorySecurity:
    def __init__(self):
        self.ip_requests: Dict[str, list] = {}  # IP -> lista de timestamps
        self.blocked_ips: Dict[str, datetime] = {}  # IP -> tempo de bloqueio
        self.failed_requests: Dict[str, int] = {}  # IP -> contagem de falhas
        security_logger.info("Sistema de segurança em memória inicializado")
    
    def is_ip_blocked(self, ip: str) -> bool:
        """
        Verifica se um IP está bloqueado.
        """
        try:
            if ip in self.blocked_ips:
                block_time = self.blocked_ips[ip]
                if datetime.now() < block_time:
                    security_logger.warning(f"IP bloqueado: {ip}")
                    return True
                else:
                    # Remove o IP da lista de bloqueados
                    del self.blocked_ips[ip]
                    security_logger.info(f"Bloqueio expirado para IP: {ip}")
            return False
        except Exception as e:
            security_logger.error(f"Erro ao verificar bloqueio de IP: {e}")
            return False
    
    def check_rate_limit(self, ip: str) -> bool:
        """
        Verifica se um IP excedeu o limite de requisições.
        """
        try:
            now = datetime.now()
            
            # Remove timestamps antigos
            if ip in self.ip_requests:
                self.ip_requests[ip] = [
                    ts for ts in self.ip_requests[ip]
                    if now - ts < timedelta(seconds=settings.SECURITY_RATE_LIMIT_PERIOD)
                ]
            
            # Verifica se o IP está bloqueado
            if self.is_ip_blocked(ip):
                return False
            
            # Inicializa a lista de timestamps se necessário
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []
            
            # Adiciona o timestamp atual
            self.ip_requests[ip].append(now)
            
            # Verifica se excedeu o limite
            if len(self.ip_requests[ip]) > settings.SECURITY_RATE_LIMIT_REQUESTS:
                security_logger.warning(f"Limite de requisições excedido para IP: {ip}")
                self.block_ip(ip)
                return False
            
            security_logger.info(f"Requisição permitida de IP: {ip}")
            return True
        except Exception as e:
            security_logger.error(f"Erro ao verificar limite de requisições: {e}")
            return False
    
    def block_ip(self, ip: str) -> None:
        """
        Bloqueia um IP por um período determinado.
        """
        try:
            block_until = datetime.now() + timedelta(seconds=settings.SECURITY_IP_BLOCK_DURATION)
            self.blocked_ips[ip] = block_until
            security_logger.warning(f"IP bloqueado até {block_until}: {ip}")
        except Exception as e:
            security_logger.error(f"Erro ao bloquear IP: {e}")
    
    def record_failed_request(self, ip: str) -> None:
        """
        Registra uma requisição falha para um IP.
        """
        try:
            if ip not in self.failed_requests:
                self.failed_requests[ip] = 0
            
            self.failed_requests[ip] += 1
            
            if self.failed_requests[ip] >= settings.SECURITY_MAX_FAILED_REQUESTS:
                security_logger.warning(f"Máximo de falhas excedido para IP: {ip}")
                self.block_ip(ip)
            
            security_logger.info(f"Falha registrada para IP: {ip}")
        except Exception as e:
            security_logger.error(f"Erro ao registrar falha: {e}")
    
    def validate_url(self, url: str) -> bool:
        """
        Valida uma URL.
        """
        try:
            # Verifica o comprimento máximo
            if len(url) > settings.SECURITY_MAX_URL_LENGTH:
                security_logger.warning(f"URL muito longa: {len(url)} caracteres")
                return False
            
            # Verifica se a URL começa com um protocolo permitido
            parsed = urlparse(url)
            if parsed.scheme not in settings.SECURITY_ALLOWED_SCHEMES:
                security_logger.warning(f"Esquema não permitido: {parsed.scheme}")
                return False
            
            # Verifica se o domínio está bloqueado
            if parsed.netloc in settings.SECURITY_BLOCKED_DOMAINS:
                security_logger.warning(f"Domínio bloqueado: {parsed.netloc}")
                return False
            
            security_logger.info(f"URL válida: {url}")
            return True
        except Exception as e:
            security_logger.error(f"Erro ao validar URL: {e}")
            return False
    
    def sanitize_url(self, url: str) -> str:
        """
        Sanitiza uma URL.
        """
        try:
            # Remove espaços em branco
            url = url.strip()
            
            # Garante que a URL começa com https:// se não tiver protocolo
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            
            security_logger.info(f"URL sanitizada: {url}")
            return url
        except Exception as e:
            security_logger.error(f"Erro ao sanitizar URL: {e}")
            return url 