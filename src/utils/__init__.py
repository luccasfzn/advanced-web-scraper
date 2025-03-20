"""
Utilitários e helpers para o web scraper.
"""

from src.utils.logger import setup_logger, get_logger
from src.utils.user_agents import get_random_user_agent, get_user_agents
from src.utils.config_manager import ConfigManager
from src.utils.concurrency import run_parallel, run_sequential

__all__ = [
    'setup_logger',
    'get_logger',
    'get_random_user_agent',
    'get_user_agents',
    'ConfigManager',
    'run_parallel',
    'run_sequential'
]
