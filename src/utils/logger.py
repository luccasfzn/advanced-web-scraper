"""
Módulo de logging configurável para o web scraper.
"""
import os
import logging
import colorlog
from datetime import datetime

class ScraperLogger:
    """Configuração de logging para o scraper com suporte a cores e múltiplos destinos."""
    
    def __init__(self, name="webscraper", log_dir="logs", console_level=logging.INFO, file_level=logging.DEBUG):
        """
        Inicializa o logger com saída para arquivo e console.
        
        Args:
            name: Nome do logger
            log_dir: Diretório para armazenar os logs
            console_level: Nível de log para o console
            file_level: Nível de log para o arquivo
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Nível base (captura tudo)
        self.logger.handlers = []  # Limpa handlers existentes
        
        # Garantir que o diretório de log existe
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Nome do arquivo de log baseado na data
        log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # Handler para console colorido
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(console_level)
        console_format = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_format)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(file_level)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        
        # Adicionar handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
    def get_logger(self):
        """Retorna o objeto logger configurado."""
        return self.logger

# Instância de logger global
_default_logger = None

def setup_logger(name="webscraper", log_dir="logs", console_level=logging.INFO, file_level=logging.DEBUG):
    """
    Configura e retorna uma instância de logger.
    
    Args:
        name: Nome do logger
        log_dir: Diretório para armazenar os logs
        console_level: Nível de log para o console
        file_level: Nível de log para o arquivo
        
    Returns:
        Objeto logger configurado
    """
    global _default_logger
    _default_logger = ScraperLogger(name, log_dir, console_level, file_level)
    return _default_logger.get_logger()

def get_logger():
    """
    Retorna o logger configurado. Se nenhum logger foi configurado, 
    cria um novo com configurações padrão.
    
    Returns:
        Objeto logger configurado
    """
    global _default_logger
    if _default_logger is None:
        return setup_logger()
    return _default_logger.get_logger()
