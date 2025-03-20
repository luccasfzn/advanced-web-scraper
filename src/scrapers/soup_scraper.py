"""
Implementação de scraper usando BeautifulSoup para páginas estáticas.
"""
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class SoupScraper(BaseScraper):
    """Scraper baseado em BeautifulSoup para páginas HTML estáticas."""
    
    def __init__(self, config):
        """
        Inicializa o scraper BeautifulSoup.
        
        Args:
            config: Dicionário de configuração do scraper
        """
        super().__init__(config)
        self.logger = logging.getLogger("webscraper")
        self.selectors = config.get("scraper_settings", {}).get("selectors", {})
        self.parser = config.get("scraper_settings", {}).get("parser", "html.parser")
        
    def scrape(self, url):
        """
        Extrai dados de uma URL usando BeautifulSoup.
        
        Args:
            url: URL para fazer scraping
            
        Returns:
            Dicionário com os dados extraídos
        """
        response = self._make_request(url)
        return self.parse_response(response)
        
    def parse_response(self, response):
        """
        Analisa a resposta HTML usando BeautifulSoup.
        
        Args:
            response: Resposta HTTP com conteúdo HTML
            
        Returns:
            Dicionário com os dados extraídos
        """
        soup = BeautifulSoup(response.content, self.parser)
        self.logger.debug(f"Página carregada com BeautifulSoup usando parser: {self.parser}")
        
        # Inicializar resultado
        result = {}
        
        # Extrair dados baseados nos seletores configurados
        for field, selector_info in self.selectors.items():
            selector = selector_info.get("selector")
            selector_type = selector_info.get("type", "css")
            attribute = selector_info.get("attribute", None)
            multiple = selector_info.get("multiple", False)
            
            try:
                if selector_type.lower() == "css":
                    elements = soup.select(selector)
                elif selector_type.lower() == "xpath":
                    # BeautifulSoup não suporta XPath diretamente, usar uma abordagem alternativa
                    self.logger.warning("XPath não é diretamente suportado pelo BeautifulSoup. Use CSS selectors.")
                    elements = []
                else:
                    self.logger.warning(f"Tipo de seletor desconhecido: {selector_type}")
                    elements = []
                
                if multiple:
                    # Extrair múltiplos elementos
                    if attribute:
                        result[field] = [elem.get(attribute) for elem in elements if elem.get(attribute)]
                    else:
                        result[field] = [elem.get_text(strip=True) for elem in elements if elem.get_text(strip=True)]
                else:
                    # Extrair um único elemento
                    if elements:
                        if attribute:
                            result[field] = elements[0].get(attribute)
                        else:
                            result[field] = elements[0].get_text(strip=True)
                    else:
                        result[field] = None
                        
            except Exception as e:
                self.logger.error(f"Erro ao extrair campo '{field}' com seletor '{selector}': {str(e)}")
                result[field] = None
        
        # Extrair metadados da página
        result["title"] = soup.title.string if soup.title else None
        result["page_length"] = len(response.content)
        
        return result

    def extract_by_selector(self, html_content, field_selectors=None):
        """
        Extrai dados de um conteúdo HTML usando seletores personalizados.
        
        Args:
            html_content: Conteúdo HTML para analisar
            field_selectors: Dicionário de seletores para campos específicos
            
        Returns:
            Dicionário com os dados extraídos
        """
        selectors = field_selectors or self.selectors
        soup = BeautifulSoup(html_content, self.parser)
        result = {}
        
        for field, selector_info in selectors.items():
            selector = selector_info.get("selector")
            attribute = selector_info.get("attribute", None)
            multiple = selector_info.get("multiple", False)
            
            try:
                elements = soup.select(selector)
                
                if multiple:
                    if attribute:
                        result[field] = [elem.get(attribute) for elem in elements if elem.get(attribute)]
                    else:
                        result[field] = [elem.get_text(strip=True) for elem in elements if elem.get_text(strip=True)]
                else:
                    if elements:
                        if attribute:
                            result[field] = elements[0].get(attribute)
                        else:
                            result[field] = elements[0].get_text(strip=True)
                    else:
                        result[field] = None
                        
            except Exception as e:
                self.logger.error(f"Erro ao extrair campo '{field}' com seletor '{selector}': {str(e)}")
                result[field] = None
                
        return result
