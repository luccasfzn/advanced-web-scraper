"""
Módulo de utilidades para o web scraper.

Este módulo contém funções e classes auxiliares utilizadas
pelos módulos de scraping, exportação e outros componentes do sistema.
"""

from src.utils.logger import setup_logger, get_logger
from src.utils.user_agents import get_random_user_agent, get_user_agents
from src.utils.config_manager import ConfigManager
from src.utils.concurrency import run_parallel, run_sequential
from src.utils.trigger import setup_trigger, start_trigger

__all__ = [
    'setup_logger',
    'get_logger',
    'get_random_user_agent',
    'get_user_agents',
    'ConfigManager',
    'run_parallel',
    'run_sequential',
    'setup_trigger',
    'start_trigger'
]
