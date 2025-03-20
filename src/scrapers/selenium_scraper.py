"""
Implementação de scraper usando Selenium para páginas dinâmicas.
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

class SeleniumScraper(BaseScraper):
    """Scraper baseado em Selenium para páginas com conteúdo dinâmico."""
    
    def __init__(self, config):
        """
        Inicializa o scraper Selenium.
        
        Args:
            config: Dicionário de configuração do scraper
        """
        super().__init__(config)
        self.logger = logging.getLogger("webscraper")
        self.selectors = config.get("scraper_settings", {}).get("selectors", {})
        self.headless = config.get("scraper_settings", {}).get("headless", True)
        self.driver = None
        self.wait_time = config.get("scraper_settings", {}).get("wait_time", 10)
        
        # Inicializar o driver na primeira chamada de scrape
        self._setup_driver()
        
    def _setup_driver(self):
        """Configura o driver Selenium."""
        try:
            self.logger.info("Inicializando driver do Selenium")
            
            # Configurar opções do Chrome
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless=new")  # Novo modo headless
                
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Adicionar user-agent para evitar detecção de bot
            chrome_options.add_argument(f'user-agent={self.ua_manager.get_random_user_agent()}')
            
            # Configurar proxy se disponível
            if self.proxy:
                chrome_options.add_argument(f'--proxy-server={self.proxy}')
            
            # Inicializar driver com webdriver-manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            
            self.logger.info("Driver do Selenium inicializado com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao inicializar driver do Selenium: {str(e)}")
            raise
    
    def _close_driver(self):
        """Fecha o driver Selenium se estiver aberto."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Driver do Selenium fechado")
            except Exception as e:
                self.logger.error(f"Erro ao fechar driver do Selenium: {str(e)}")
            finally:
                self.driver = None
                
    def __del__(self):
        """Destrutor da classe, garante que o driver seja fechado."""
        self._close_driver()
        
    def scrape(self, url):
        """
        Extrai dados de uma URL usando Selenium.
        
        Args:
            url: URL para fazer scraping
            
        Returns:
            Dicionário com os dados extraídos
        """
        if not self.driver:
            self._setup_driver()
            
        try:
            self.logger.info(f"Navegando para: {url}")
            self.driver.get(url)
            
            # Esperar pelo carregamento da página
            time.sleep(2)  # Espera inicial
            
            # Executar scrolling para carregar conteúdo lazy-load, se necessário
            self._scroll_page()
            
            # Processar a página
            return self.parse_response(self.driver)
            
        except Exception as e:
            self.logger.error(f"Erro no scraping com Selenium para {url}: {str(e)}")
            raise
            
    def _scroll_page(self, scroll_pause_time=1.0, max_scrolls=3):
        """
        Executa scrolling na página para carregar conteúdo lazy-load.
        
        Args:
            scroll_pause_time: Tempo de pausa entre scrolls
            max_scrolls: Número máximo de scrolls a executar
        """
        try:
            # Scroll down para carregar conteúdo lazy
            for i in range(max_scrolls):
                # Scroll até o fim da página
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Pausar para carregar o conteúdo
                time.sleep(scroll_pause_time)
                
            # Voltar ao topo
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
        except Exception as e:
            self.logger.warning(f"Erro durante o scrolling da página: {str(e)}")
        
    def parse_response(self, driver):
        """
        Analisa a página carregada pelo Selenium.
        
        Args:
            driver: Instância do WebDriver com a página carregada
            
        Returns:
            Dicionário com os dados extraídos
        """
        result = {}
        
        # Extrair dados baseados nos seletores configurados
        for field, selector_info in self.selectors.items():
            selector = selector_info.get("selector")
            selector_type = selector_info.get("type", "css")
            attribute = selector_info.get("attribute", None)
            multiple = selector_info.get("multiple", False)
            wait = selector_info.get("wait", False)
            
            try:
                # Esperar pelo elemento se necessário
                if wait:
                    wait_method = selector_info.get("wait_method", "presence")
                    if wait_method == "presence":
                        condition = EC.presence_of_element_located
                    elif wait_method == "visible":
                        condition = EC.visibility_of_element_located
                    elif wait_method == "clickable":
                        condition = EC.element_to_be_clickable
                    else:
                        condition = EC.presence_of_element_located
                        
                    if selector_type.lower() == "css":
                        WebDriverWait(driver, self.wait_time).until(
                            condition((By.CSS_SELECTOR, selector))
                        )
                    elif selector_type.lower() == "xpath":
                        WebDriverWait(driver, self.wait_time).until(
                            condition((By.XPATH, selector))
                        )
                
                # Localizar elementos
                if selector_type.lower() == "css":
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                elif selector_type.lower() == "xpath":
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    self.logger.warning(f"Tipo de seletor desconhecido: {selector_type}")
                    elements = []
                
                # Extrair valores
                if multiple:
                    if attribute:
                        if attribute == "text":
                            result[field] = [elem.text.strip() for elem in elements if elem.text.strip()]
                        else:
                            result[field] = [elem.get_attribute(attribute) for elem in elements if elem.get_attribute(attribute)]
                    else:
                        result[field] = [elem.text.strip() for elem in elements if elem.text.strip()]
                else:
                    if elements:
                        if attribute:
                            if attribute == "text":
                                result[field] = elements[0].text.strip()
                            else:
                                result[field] = elements[0].get_attribute(attribute)
                        else:
                            result[field] = elements[0].text.strip()
                    else:
                        result[field] = None
                        
            except Exception as e:
                self.logger.error(f"Erro ao extrair campo '{field}' com seletor '{selector}': {str(e)}")
                result[field] = None
        
        # Extrair metadados da página
        result["title"] = driver.title
        result["current_url"] = driver.current_url
        
        # Capturar screenshots se necessário
        if self.config.get("scraper_settings", {}).get("capture_screenshot", False):
            timestamp = int(time.time())
            screenshot_path = f"screenshots/screenshot_{timestamp}.png"
            try:
                driver.save_screenshot(screenshot_path)
                result["screenshot_path"] = screenshot_path
            except Exception as e:
                self.logger.error(f"Erro ao capturar screenshot: {str(e)}")
        
        return result
        
    def extract_with_javascript(self, url, javascript_code=None):
        """
        Extrai dados executando código JavaScript customizado.
        
        Args:
            url: URL para fazer scraping
            javascript_code: Código JavaScript para executar na página
            
        Returns:
            Resultado da execução do JavaScript
        """
        if not self.driver:
            self._setup_driver()
            
        try:
            self.driver.get(url)
            time.sleep(2)  # Espera pela carga
            
            if not javascript_code:
                # Código JavaScript padrão para extrair informações básicas
                javascript_code = """
                return {
                    title: document.title,
                    meta: Array.from(document.querySelectorAll('meta')).map(m => ({
                        name: m.getAttribute('name') || m.getAttribute('property'),
                        content: m.getAttribute('content')
                    })).filter(m => m.name && m.content),
                    links: Array.from(document.querySelectorAll('a')).map(a => a.href).slice(0, 20),
                    images: Array.from(document.querySelectorAll('img')).map(img => img.src).slice(0, 20)
                };
                """
                
            # Executar JavaScript
            result = self.driver.execute_script(javascript_code)
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair dados com JavaScript de {url}: {str(e)}")
            raise
