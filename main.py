#!/usr/bin/env python
"""
Advanced Web Scraper - Script principal

Este script é o ponto de entrada para executar o scraper com diferentes configurações.
Permite extrair informações de produtos e categorias de diversos sites de e-commerce.
"""
import os
import sys
import argparse
import logging
import json
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar componentes do scraper
from src.utils.logger import ScraperLogger
from src.utils.config_manager import ConfigManager
from src.utils.concurrency import ScraperConcurrencyManager
from src.scrapers.soup_scraper import SoupScraper
from src.scrapers.selenium_scraper import SeleniumScraper
from src.exporters.csv_exporter import CSVExporter
from src.exporters.json_exporter import JSONExporter

def parse_arguments():
    """Processa os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(description='Advanced Web Scraper')
    parser.add_argument('--config', type=str, default='config/barbara_porto.json',
                        help='Caminho para o arquivo de configuração')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Diretório para salvar os resultados (sobrescreve o valor na configuração)')
    parser.add_argument('--max-workers', type=int, default=None,
                        help='Número máximo de workers para processamento paralelo')
    parser.add_argument('--headless', action='store_true', default=None,
                        help='Executar em modo headless (sem interface gráfica)')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Nível de log')
    parser.add_argument('--single-url', type=str, default=None,
                        help='URL única para scraping (para testes)')
    
    return parser.parse_args()

def setup_logging(log_level):
    """Configura o sistema de logging."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    console_level = log_level_map.get(log_level, logging.INFO)
    logger_setup = ScraperLogger(name="webscraper", log_dir=log_dir, 
                                console_level=console_level, 
                                file_level=logging.DEBUG)
    
    return logger_setup.get_logger()

def get_appropriate_exporter(format_name, output_dir, filename_prefix):
    """Retorna o exportador apropriado para o formato especificado."""
    if format_name.lower() == 'csv':
        return CSVExporter(output_dir=output_dir, filename_prefix=filename_prefix)
    elif format_name.lower() == 'json':
        return JSONExporter(output_dir=output_dir, filename_prefix=filename_prefix)
    else:
        raise ValueError(f"Formato de exportação não suportado: {format_name}")

def get_appropriate_scraper(config):
    """Retorna o scraper apropriado baseado na configuração."""
    if config.get("scraper_settings", {}).get("use_selenium", False):
        return SeleniumScraper(config)
    else:
        return SoupScraper(config)

def main():
    """Função principal do scraper."""
    # Processar argumentos
    args = parse_arguments()
    
    # Configurar logging
    logger = setup_logging(args.log_level)
    logger.info("Iniciando Advanced Web Scraper")
    
    try:
        # Carregar configuração
        config_manager = ConfigManager(args.config)
        config = config_manager.get_config()
        logger.info(f"Configuração carregada de: {args.config}")
        
        # Sobrescrever configurações com argumentos da linha de comando
        if args.output_dir:
            config["export_settings"]["output_dir"] = args.output_dir
            logger.info(f"Output dir sobrescrito para: {args.output_dir}")
            
        if args.max_workers:
            config["scraper_settings"]["max_workers"] = args.max_workers
            logger.info(f"Max workers sobrescrito para: {args.max_workers}")
            
        if args.headless is not None:
            config["scraper_settings"]["headless"] = args.headless
            logger.info(f"Modo headless definido como: {args.headless}")
            
        # Configurar URLs para processamento
        urls_to_process = []
        if args.single_url:
            urls_to_process = [args.single_url]
            logger.info(f"Processando URL única: {args.single_url}")
        else:
            urls_to_process = config["urls"]
            logger.info(f"Processando {len(urls_to_process)} URLs da configuração")
        
        # Obter o scraper apropriado
        scraper = get_appropriate_scraper(config)
        logger.info(f"Usando scraper: {scraper.__class__.__name__}")
        
        # Configurar gerenciador de concorrência
        scraper_settings = config.get("scraper_settings", {})
        concurrency_manager = ScraperConcurrencyManager(
            max_workers=scraper_settings.get("max_workers", 4),
            min_delay=scraper_settings.get("min_delay", 1.0),
            max_delay=scraper_settings.get("max_delay", 3.0)
        )
        
        # Executar scraping
        logger.info("Iniciando processo de scraping")
        results = concurrency_manager.process_batch(
            urls=urls_to_process,
            process_func=scraper.extract_data,
            desc="Extraindo dados dos produtos"
        )
        
        logger.info(f"Extração concluída. {len(results)} resultados obtidos.")
        
        # Classificar em categorias se necessário
        if "categories" in config:
            categories = config["categories"]
            for item in results:
                url = item.get("url", "").lower()
                item_category = "Sem categoria"
                
                for category_name, keywords in categories.items():
                    if any(keyword.lower() in url for keyword in keywords):
                        item_category = category_name
                        break
                        
                item["categoria_inferida"] = item_category
        
        # Exportar resultados
        export_settings = config.get("export_settings", {})
        output_dir = export_settings.get("output_dir", "data")
        filename_prefix = export_settings.get("filename_prefix", "scraper_result")
        
        # Timestamp para nomear os arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Exportar para todos os formatos configurados
        for format_name in export_settings.get("formats", ["csv"]):
            try:
                exporter = get_appropriate_exporter(format_name, output_dir, filename_prefix)
                filename = f"{filename_prefix}_{timestamp}.{format_name.lower()}"
                output_path = exporter.export(results, filename)
                logger.info(f"Dados exportados para {format_name}: {output_path}")
            except Exception as e:
                logger.error(f"Erro ao exportar para {format_name}: {str(e)}")
        
        logger.info("Processamento concluído com sucesso!")
        return 0
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}", exc_info=True)
        return 1
    finally:
        # Limpar recursos se necessário
        logger.info("Finalizando Advanced Web Scraper")
        
if __name__ == "__main__":
    sys.exit(main())
