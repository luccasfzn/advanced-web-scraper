"""
Módulo de scrapers para diferentes sites e APIs.

Este módulo contém implementações específicas para extração de dados
de várias fontes, incluindo sites e APIs públicas.
"""

from src.scrapers.base_scraper import BaseScraper
from src.scrapers.soup_scraper import SoupScraper
from src.scrapers.selenium_scraper import SeleniumScraper

__all__ = [
    'BaseScraper',
    'SoupScraper',
    'SeleniumScraper'
]
