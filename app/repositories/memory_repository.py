from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from app.core.logging import memory_logger

class MemoryRepository:
    def __init__(self):
        self.urls: Dict[str, str] = {}
        self.stats: Dict[str, dict] = {}
        self.data_file = "data/urls.json"
        
        # Cria o diretório de dados se não existir
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Carrega os dados do arquivo
        self._load_data()
        
        memory_logger.info("Repositório em memória inicializado")
    
    def _load_data(self) -> None:
        """
        Carrega os dados do arquivo JSON.
        """
        try:
            if os.path.exists(self.data_file):
                memory_logger.debug(f"Carregando dados do arquivo: {self.data_file}")
                
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    
                self.urls = data.get("urls", {})
                self.stats = data.get("stats", {})
                
                # Converte as strings de data para objetos datetime
                for short_code, stat in self.stats.items():
                    if "created_at" in stat and stat["created_at"]:
                        stat["created_at"] = datetime.fromisoformat(stat["created_at"])
                    if "last_accessed" in stat and stat["last_accessed"]:
                        stat["last_accessed"] = datetime.fromisoformat(stat["last_accessed"])
                
                memory_logger.info(f"Dados carregados com sucesso: {len(self.urls)} URLs")
            else:
                memory_logger.debug("Arquivo de dados não encontrado, iniciando com repositório vazio")
        except Exception as e:
            memory_logger.error(f"Erro ao carregar dados: {e}")
    
    def _save_data(self) -> None:
        """
        Salva os dados no arquivo JSON.
        """
        try:
            memory_logger.debug(f"Salvando dados no arquivo: {self.data_file}")
            
            # Converte os objetos datetime para strings ISO
            stats_to_save = {}
            for short_code, stat in self.stats.items():
                stats_to_save[short_code] = stat.copy()
                if "created_at" in stat and stat["created_at"]:
                    stats_to_save[short_code]["created_at"] = stat["created_at"].isoformat()
                if "last_accessed" in stat and stat["last_accessed"]:
                    stats_to_save[short_code]["last_accessed"] = stat["last_accessed"].isoformat()
            
            data = {
                "urls": self.urls,
                "stats": stats_to_save
            }
            
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=2)
            
            memory_logger.info(f"Dados salvos com sucesso: {len(self.urls)} URLs")
        except Exception as e:
            memory_logger.error(f"Erro ao salvar dados: {e}")
    
    def save_url(self, short_code: str, original_url: str) -> bool:
        """
        Salva o mapeamento entre código curto e URL original.
        """
        try:
            memory_logger.debug(f"Salvando URL: {short_code} -> {original_url}")
            
            # Salva a URL
            self.urls[short_code] = original_url
            
            # Inicializa as estatísticas
            self.stats[short_code] = {
                "access_count": 0,
                "created_at": datetime.utcnow(),
                "last_accessed": None
            }
            
            # Salva os dados no arquivo
            self._save_data()
            
            memory_logger.info(f"URL salva com sucesso: {short_code}")
            return True
        except Exception as e:
            memory_logger.error(f"Erro ao salvar URL: {e}")
            return False
    
    def get_url(self, short_code: str) -> Optional[str]:
        """
        Recupera a URL original a partir do código curto.
        """
        try:
            memory_logger.debug(f"Buscando URL para o código: {short_code}")
            url = self.urls.get(short_code)
            
            if url:
                memory_logger.info(f"URL encontrada: {short_code} -> {url}")
            else:
                memory_logger.warning(f"URL não encontrada para o código: {short_code}")
                
            return url
        except Exception as e:
            memory_logger.error(f"Erro ao buscar URL: {e}")
            return None
    
    def increment_access_count(self, short_code: str) -> bool:
        """
        Incrementa o contador de acessos de uma URL.
        """
        try:
            memory_logger.debug(f"Incrementando contador de acessos: {short_code}")
            
            if short_code in self.stats:
                self.stats[short_code]["access_count"] += 1
                memory_logger.debug(f"Contador de acessos atualizado: {short_code} -> {self.stats[short_code]['access_count']}")
                
                # Salva os dados no arquivo
                self._save_data()
                
                return True
            return False
        except Exception as e:
            memory_logger.error(f"Erro ao incrementar contador de acessos: {e}")
            return False
    
    def update_last_accessed(self, short_code: str) -> bool:
        """
        Atualiza a data do último acesso a uma URL.
        """
        try:
            memory_logger.debug(f"Atualizando último acesso: {short_code}")
            
            if short_code in self.stats:
                self.stats[short_code]["last_accessed"] = datetime.utcnow()
                memory_logger.debug(f"Último acesso atualizado: {short_code}")
                
                # Salva os dados no arquivo
                self._save_data()
                
                return True
            return False
        except Exception as e:
            memory_logger.error(f"Erro ao atualizar último acesso: {e}")
            return False
    
    def get_stats(self, short_code: str) -> Optional[dict]:
        """
        Obtém estatísticas de uma URL.
        """
        try:
            memory_logger.debug(f"Buscando estatísticas para URL: {short_code}")
            
            if short_code not in self.stats:
                memory_logger.warning(f"Estatísticas não encontradas para URL: {short_code}")
                return None
            
            memory_logger.debug(f"Estatísticas encontradas para URL: {short_code}")
            return self.stats[short_code]
        except Exception as e:
            memory_logger.error(f"Erro ao buscar estatísticas: {e}")
            return None
    
    def list_urls(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """
        Lista URLs com paginação.
        """
        try:
            memory_logger.debug(f"Listando URLs (skip={skip}, limit={limit})")
            
            # Obtém todos os códigos curtos
            all_codes = list(self.urls.items())
            
            # Aplica paginação
            paginated_codes = all_codes[skip:skip+limit]
            
            # Obtém as estatísticas de cada URL
            urls = []
            for code, url in paginated_codes:
                stats = self.stats.get(code, {})
                urls.append({
                    "short_code": code,
                    "original_url": url,
                    "access_count": stats.get("access_count", 0),
                    "created_at": stats.get("created_at"),
                    "last_accessed": stats.get("last_accessed")
                })
            
            memory_logger.debug(f"Listagem de URLs obtida: {len(urls)} URLs")
            return urls
        except Exception as e:
            memory_logger.error(f"Erro ao listar URLs: {e}")
            return []
    
    def count_urls(self) -> int:
        """
        Conta o número total de URLs.
        """
        try:
            memory_logger.debug("Contando total de URLs")
            
            count = len(self.urls)
            memory_logger.debug(f"Total de URLs: {count}")
            
            return count
        except Exception as e:
            memory_logger.error(f"Erro ao contar URLs: {e}")
            return 0
    
    def delete_url(self, short_code: str) -> bool:
        """
        Exclui uma URL.
        """
        try:
            memory_logger.debug(f"Excluindo URL: {short_code}")
            
            # Verifica se a URL existe
            if short_code not in self.urls:
                memory_logger.warning(f"URL não encontrada para exclusão: {short_code}")
                return False
            
            # Remove a URL e suas estatísticas
            del self.urls[short_code]
            if short_code in self.stats:
                del self.stats[short_code]
            
            # Salva os dados no arquivo
            self._save_data()
            
            memory_logger.info(f"URL excluída com sucesso: {short_code}")
            return True
        except Exception as e:
            memory_logger.error(f"Erro ao excluir URL: {e}")
            return False
    
    def update_url(self, short_code: str, new_url: str) -> bool:
        """
        Atualiza uma URL.
        """
        try:
            memory_logger.debug(f"Atualizando URL: {short_code} -> {new_url}")
            
            # Verifica se a URL existe
            if short_code not in self.urls:
                memory_logger.warning(f"URL não encontrada para atualização: {short_code}")
                return False
            
            # Atualiza a URL
            self.urls[short_code] = new_url
            
            # Atualiza as estatísticas
            if short_code in self.stats:
                self.stats[short_code]["original_url"] = new_url
            
            # Salva os dados no arquivo
            self._save_data()
            
            memory_logger.info(f"URL atualizada com sucesso: {short_code}")
            return True
        except Exception as e:
            memory_logger.error(f"Erro ao atualizar URL: {e}")
            return False
    
    def health_check(self) -> bool:
        """
        Verifica se o repositório está funcionando.
        """
        try:
            memory_logger.debug("Verificando saúde do repositório")
            
            # Tenta salvar e carregar os dados
            self._save_data()
            self._load_data()
            
            memory_logger.info("Saúde do repositório verificada com sucesso")
            return True
        except Exception as e:
            memory_logger.error(f"Erro ao verificar saúde do repositório: {e}")
            return False 