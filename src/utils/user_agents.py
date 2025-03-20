"""
Utilitário para rotação de user-agents.
"""
import random
import logging
from fake_useragent import UserAgent

class UserAgentManager:
    """Gerencia a rotação de user-agents para evitar bloqueios."""
    
    def __init__(self, use_fake_ua=True, custom_agents=None):
        """
        Inicializa o gerenciador de user-agents.
        
        Args:
            use_fake_ua: Se True, usa a biblioteca fake-useragent
            custom_agents: Lista opcional de user-agents personalizados
        """
        self.logger = logging.getLogger("webscraper")
        self.custom_agents = custom_agents or []
        self.use_fake_ua = use_fake_ua
        self.fake_ua = None
        
        if use_fake_ua:
            try:
                self.fake_ua = UserAgent()
                self.logger.info("Fake UserAgent iniciado com sucesso")
            except Exception as e:
                self.logger.warning(f"Erro ao iniciar Fake UserAgent: {e}")
                self.use_fake_ua = False
                
        # User-agents de fallback caso fake-useragent falhe
        if not self.custom_agents:
            self.custom_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
            ]

    def get_random_user_agent(self):
        """Retorna um user-agent aleatório."""
        if self.use_fake_ua and self.fake_ua:
            try:
                return self.fake_ua.random
            except Exception as e:
                self.logger.warning(f"Erro ao obter user-agent da fake-useragent: {e}")
        
        # Fallback para a lista personalizada
        return random.choice(self.custom_agents)
    
    def get_header(self, additional_headers=None):
        """
        Retorna um conjunto de headers HTTP com um user-agent aleatório.
        
        Args:
            additional_headers: Headers adicionais a serem incluídos
            
        Returns:
            Dicionário com os headers
        """
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',  # Do Not Track
        }
        
        # Adicionar headers extras se fornecidos
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
