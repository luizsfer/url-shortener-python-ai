from datetime import datetime
from typing import List, Optional
import hashlib
from app.repositories.memory_repository import MemoryRepository
from app.core.logging import url_logger

class URLService:
    def __init__(self):
        self.repository = MemoryRepository()
        url_logger.info("Serviço de URL inicializado com repositório em memória")
    
    def shorten_url(self, original_url: str) -> str:
        """
        Encurta uma URL e salva no repositório.
        """
        try:
            url_logger.debug(f"Encurtando URL: {original_url}")
            
            # Gera o código curto
            short_code = self._generate_short_code(original_url)
            
            # Salva no repositório
            self.repository.save_url(short_code, original_url)
            
            url_logger.info(f"URL encurtada com sucesso: {short_code}")
            return short_code
        except Exception as e:
            url_logger.error(f"Erro ao encurtar URL: {e}")
            raise
    
    def get_url(self, short_code: str) -> Optional[str]:
        """
        Recupera a URL original a partir do código curto.
        """
        try:
            url_logger.debug(f"Buscando URL para o código: {short_code}")
            
            # Busca a URL
            url = self.repository.get_url(short_code)
            
            if url:
                # Atualiza estatísticas
                self.repository.increment_access_count(short_code)
                self.repository.update_last_accessed(short_code)
                
                url_logger.info(f"URL encontrada: {short_code} -> {url}")
            else:
                url_logger.warning(f"URL não encontrada para o código: {short_code}")
            
            return url
        except Exception as e:
            url_logger.error(f"Erro ao buscar URL: {e}")
            raise
    
    def get_url_stats(self, short_code: str) -> Optional[dict]:
        """
        Obtém estatísticas de uma URL.
        """
        try:
            url_logger.debug(f"Buscando estatísticas para URL: {short_code}")
            
            stats = self.repository.get_url_stats(short_code)
            if not stats:
                url_logger.warning(f"Estatísticas não encontradas para URL: {short_code}")
                return None
            
            url_logger.debug(f"Estatísticas encontradas para URL: {short_code}")
            return stats
        except Exception as e:
            url_logger.error(f"Erro ao buscar estatísticas: {e}")
            raise
    
    def list_urls(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """
        Lista URLs com paginação.
        """
        try:
            url_logger.debug(f"Listando URLs (skip={skip}, limit={limit})")
            
            urls = self.repository.list_urls(skip, limit)
            url_logger.debug(f"Listagem de URLs obtida: {len(urls)} URLs")
            
            return urls
        except Exception as e:
            url_logger.error(f"Erro ao listar URLs: {e}")
            raise
    
    def count_urls(self) -> int:
        """
        Conta o número total de URLs.
        """
        try:
            url_logger.debug("Contando total de URLs")
            
            count = self.repository.count_urls()
            url_logger.debug(f"Total de URLs: {count}")
            
            return count
        except Exception as e:
            url_logger.error(f"Erro ao contar URLs: {e}")
            raise
    
    def delete_url(self, short_code: str) -> bool:
        """
        Exclui uma URL.
        """
        try:
            url_logger.debug(f"Excluindo URL: {short_code}")
            
            success = self.repository.delete_url(short_code)
            if success:
                url_logger.info(f"URL excluída com sucesso: {short_code}")
            else:
                url_logger.warning(f"URL não encontrada para exclusão: {short_code}")
            
            return success
        except Exception as e:
            url_logger.error(f"Erro ao excluir URL: {e}")
            raise
    
    def update_url(self, short_code: str, new_url: str) -> bool:
        """
        Atualiza uma URL.
        """
        try:
            url_logger.debug(f"Atualizando URL: {short_code} -> {new_url}")
            
            success = self.repository.update_url(short_code, new_url)
            if success:
                url_logger.info(f"URL atualizada com sucesso: {short_code}")
            else:
                url_logger.warning(f"URL não encontrada para atualização: {short_code}")
            
            return success
        except Exception as e:
            url_logger.error(f"Erro ao atualizar URL: {e}")
            raise
    
    def check_connection(self) -> bool:
        """
        Verifica se o repositório está funcionando.
        """
        try:
            url_logger.debug("Verificando conexão com o repositório")
            
            is_connected = self.repository.check_connection()
            if is_connected:
                url_logger.info("Conexão com o repositório verificada com sucesso")
            else:
                url_logger.error("Falha ao verificar conexão com o repositório")
            
            return is_connected
        except Exception as e:
            url_logger.error(f"Erro ao verificar conexão: {e}")
            return False
    
    def _generate_short_code(self, url: str) -> str:
        """
        Gera um código curto para a URL.
        """
        # Usa MD5 para gerar um hash da URL
        hash_object = hashlib.md5(url.encode())
        hash_hex = hash_object.hexdigest()
        
        # Pega os primeiros 7 caracteres do hash
        short_code = hash_hex[:7]
        
        return short_code 