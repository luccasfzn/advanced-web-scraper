"""
Classe base para diferentes implementações de scrapers.
"""
import time
import logging
import requests
from retry import retry
from abc import ABC, abstractmethod

from ..utils.user_agents import UserAgentManager

class BaseScraper(ABC):
    """Classe base abstrata para todos os scrapers."""
    
    def __init__(self, config):
        """
        Inicializa o scraper base.
        
        Args:
            config: Dicionário de configuração do scraper
        """
        self.config = config
        self.logger = logging.getLogger("webscraper")
        self.ua_manager = UserAgentManager()
        
        # Configurações padrão
        self.timeout = config.get("scraper_settings", {}).get("timeout", 30)
        self.retries = config.get("scraper_settings", {}).get("retries", 3)
        self.proxy = config.get("scraper_settings", {}).get("proxy", None)
        
        self.session = self._setup_session()
        
    def _setup_session(self):
        """
        Configura a sessão HTTP com configurações personalizadas.
        
        Returns:
            Sessão HTTP configurada
        """
        session = requests.Session()
        
        # Configurar proxy se fornecido
        if self.proxy:
            proxies = {
                "http": self.proxy,
                "https": self.proxy
            }
            session.proxies.update(proxies)
            self.logger.info(f"Proxy configurado: {self.proxy}")
            
        return session
        
    @retry(tries=3, delay=2, backoff=2, logger=logging.getLogger("webscraper"))
    def _make_request(self, url, method="GET", data=None, params=None, headers=None, cookies=None):
        """
        Faz uma requisição HTTP com retry automático.
        
        Args:
            url: URL para a requisição
            method: Método HTTP (GET, POST, etc.)
            data: Dados para requisições POST
            params: Parâmetros para a URL
            headers: Headers HTTP personalizados
            cookies: Cookies para a requisição
            
        Returns:
            Resposta HTTP
        """
        headers = headers or self.ua_manager.get_header()
        
        self.logger.debug(f"Fazendo requisição {method} para: {url}")
        start_time = time.time()
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                data=data,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            elapsed = time.time() - start_time
            self.logger.debug(f"Requisição concluída em {elapsed:.2f}s. Status: {response.status_code}")
            
            # Verificar se a resposta foi bem-sucedida
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro na requisição para {url}: {str(e)}")
            raise
            
    @abstractmethod
    def scrape(self, url):
        """
        Método abstrato para implementar o scraping específico.
        
        Args:
            url: URL para fazer scraping
            
        Returns:
            Dados extraídos da URL
        """
        pass
        
    @abstractmethod
    def parse_response(self, response):
        """
        Método abstrato para implementar o parsing da resposta HTTP.
        
        Args:
            response: Resposta HTTP
            
        Returns:
            Dados extraídos da resposta
        """
        pass
        
    def extract_data(self, url):
        """
        Extrai dados de uma URL usando os métodos do scraper.
        
        Args:
            url: URL para extrair dados
            
        Returns:
            Dados extraídos
        """
        try:
            self.logger.info(f"Extraindo dados de: {url}")
            result = self.scrape(url)
            result["url"] = url
            result["status"] = "success"
            return result
        except Exception as e:
            self.logger.error(f"Falha ao extrair dados de {url}: {str(e)}")
            return {
                "url": url,
                "status": "error",
                "error": str(e)
            }
