from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Configurações da aplicação
    APP_TITLE: str = "URL Shortener API"
    APP_DESCRIPTION: str = "API para encurtamento de URLs com cache em memória"
    APP_VERSION: str = "1.0.0"
    
    # Configurações de segurança
    SECURITY_RATE_LIMIT_REQUESTS: int = 100
    SECURITY_RATE_LIMIT_PERIOD: int = 3600
    SECURITY_MAX_URL_LENGTH: int = 2048
    SECURITY_MAX_REQUEST_SIZE: int = 1048576
    SECURITY_IP_BLOCK_DURATION: int = 3600
    SECURITY_MAX_FAILED_REQUESTS: int = 100
    SECURITY_ALLOWED_SCHEMES: List[str] = ["http", "https"]
    SECURITY_BLOCKED_DOMAINS: List[str] = ["localhost", "127.0.0.1"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 