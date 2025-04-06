from datetime import datetime
from typing import Dict, List, Optional
from app.core.logging import redis_logger

class MemoryRepository:
    def __init__(self):
        self.urls: Dict[str, str] = {}
        self.stats: Dict[str, dict] = {}
        self.url_codes: set = set()
        redis_logger.info("Repositório em memória inicializado")
    
    def save_url(self, short_code: str, original_url: str) -> None:
        """
        Salva o mapeamento entre código curto e URL original.
        """
        try:
            redis_logger.debug(f"Salvando URL: {short_code} -> {original_url}")
            
            # Salva a URL
            self.urls[short_code] = original_url
            
            # Inicializa as estatísticas
            stats = {
                "short_code": short_code,
                "original_url": original_url,
                "access_count": 0,
                "created_at": datetime.now().isoformat(),
                "last_accessed": None
            }
            self.stats[short_code] = stats
            
            # Adiciona à lista de URLs
            self.url_codes.add(short_code)
            
            redis_logger.info(f"URL salva com sucesso: {short_code}")
        except Exception as e:
            redis_logger.error(f"Erro ao salvar URL: {e}")
            raise
    
    def get_url(self, short_code: str) -> Optional[str]:
        """
        Recupera a URL original a partir do código curto.
        """
        try:
            redis_logger.debug(f"Buscando URL para o código: {short_code}")
            url = self.urls.get(short_code)
            
            if url:
                redis_logger.info(f"URL encontrada: {short_code} -> {url}")
            else:
                redis_logger.warning(f"URL não encontrada para o código: {short_code}")
                
            return url
        except Exception as e:
            redis_logger.error(f"Erro ao buscar URL: {e}")
            raise
    
    def increment_access_count(self, short_code: str) -> None:
        """
        Incrementa o contador de acessos de uma URL.
        """
        try:
            redis_logger.debug(f"Incrementando contador de acessos: {short_code}")
            
            if short_code in self.stats:
                self.stats[short_code]["access_count"] += 1
                redis_logger.debug(f"Contador de acessos atualizado: {short_code} -> {self.stats[short_code]['access_count']}")
        except Exception as e:
            redis_logger.error(f"Erro ao incrementar contador de acessos: {e}")
    
    def update_last_accessed(self, short_code: str) -> None:
        """
        Atualiza a data do último acesso a uma URL.
        """
        try:
            redis_logger.debug(f"Atualizando último acesso: {short_code}")
            
            if short_code in self.stats:
                self.stats[short_code]["last_accessed"] = datetime.now().isoformat()
                redis_logger.debug(f"Último acesso atualizado: {short_code}")
        except Exception as e:
            redis_logger.error(f"Erro ao atualizar último acesso: {e}")
    
    def get_url_stats(self, short_code: str) -> Optional[dict]:
        """
        Obtém estatísticas de uma URL.
        """
        try:
            redis_logger.debug(f"Buscando estatísticas para URL: {short_code}")
            
            stats = self.stats.get(short_code)
            if not stats:
                redis_logger.warning(f"Estatísticas não encontradas para URL: {short_code}")
                return None
            
            redis_logger.debug(f"Estatísticas encontradas para URL: {short_code}")
            return stats
        except Exception as e:
            redis_logger.error(f"Erro ao buscar estatísticas: {e}")
            raise
    
    def list_urls(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """
        Lista URLs com paginação.
        """
        try:
            redis_logger.debug(f"Listando URLs (skip={skip}, limit={limit})")
            
            # Obtém todos os códigos curtos
            all_codes = list(self.url_codes)
            
            # Aplica paginação
            paginated_codes = all_codes[skip:skip+limit]
            
            # Obtém as estatísticas de cada URL
            urls = []
            for code in paginated_codes:
                if code in self.stats:
                    urls.append(self.stats[code])
            
            redis_logger.debug(f"Listagem de URLs obtida: {len(urls)} URLs")
            return urls
        except Exception as e:
            redis_logger.error(f"Erro ao listar URLs: {e}")
            raise
    
    def count_urls(self) -> int:
        """
        Conta o número total de URLs.
        """
        try:
            redis_logger.debug("Contando total de URLs")
            
            count = len(self.url_codes)
            redis_logger.debug(f"Total de URLs: {count}")
            
            return count
        except Exception as e:
            redis_logger.error(f"Erro ao contar URLs: {e}")
            raise
    
    def delete_url(self, short_code: str) -> bool:
        """
        Exclui uma URL.
        """
        try:
            redis_logger.debug(f"Excluindo URL: {short_code}")
            
            # Verifica se a URL existe
            if short_code not in self.urls:
                redis_logger.warning(f"URL não encontrada para exclusão: {short_code}")
                return False
            
            # Remove a URL e suas estatísticas
            del self.urls[short_code]
            del self.stats[short_code]
            self.url_codes.remove(short_code)
            
            redis_logger.info(f"URL excluída com sucesso: {short_code}")
            return True
        except Exception as e:
            redis_logger.error(f"Erro ao excluir URL: {e}")
            raise
    
    def update_url(self, short_code: str, new_url: str) -> bool:
        """
        Atualiza uma URL.
        """
        try:
            redis_logger.debug(f"Atualizando URL: {short_code} -> {new_url}")
            
            # Verifica se a URL existe
            if short_code not in self.urls:
                redis_logger.warning(f"URL não encontrada para atualização: {short_code}")
                return False
            
            # Atualiza a URL
            self.urls[short_code] = new_url
            
            # Atualiza as estatísticas
            if short_code in self.stats:
                self.stats[short_code]["original_url"] = new_url
            
            redis_logger.info(f"URL atualizada com sucesso: {short_code}")
            return True
        except Exception as e:
            redis_logger.error(f"Erro ao atualizar URL: {e}")
            raise
    
    def check_connection(self) -> bool:
        """
        Verifica se o repositório está funcionando.
        """
        try:
            redis_logger.debug("Verificando repositório em memória")
            return True
        except Exception as e:
            redis_logger.error(f"Erro ao verificar repositório: {e}")
            return False 