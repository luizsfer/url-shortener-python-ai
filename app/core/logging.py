import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

# Cria o diretório de logs se não existir
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configuração do logger
def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """
    Configura um logger com saída para console e arquivo (opcional).
    
    Args:
        name: Nome do logger
        log_file: Caminho para o arquivo de log (opcional)
        level: Nível de log (padrão: INFO)
    
    Returns:
        Logger configurado
    """
    # Cria o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        file_handler = RotatingFileHandler(
            log_dir / log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Loggers para diferentes componentes
api_logger = setup_logger("api", "api.log")
security_logger = setup_logger("security", "security.log")
url_logger = setup_logger("url", "url.log")
redis_logger = setup_logger("redis", "redis.log") 