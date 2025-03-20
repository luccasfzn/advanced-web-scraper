"""
Implementações de scrapers para diferentes cenários de extração.
"""

from src.scrapers.base_scraper import BaseScraper
from src.scrapers.soup_scraper import SoupScraper
from src.scrapers.selenium_scraper import SeleniumScraper

__all__ = [
    'BaseScraper',
    'SoupScraper',
    'SeleniumScraper'
]
