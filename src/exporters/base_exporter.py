"""
Classe base para exportadores de dados.
"""
import os
import logging
from abc import ABC, abstractmethod

class BaseExporter(ABC):
    """Classe base para exportadores de dados."""
    
    def __init__(self, output_dir="data", filename_prefix="scraper_result"):
        """
        Inicializa o exportador base.
        
        Args:
            output_dir: Diretório de saída para os arquivos
            filename_prefix: Prefixo para os nomes dos arquivos
        """
        self.output_dir = output_dir
        self.filename_prefix = filename_prefix
        self.logger = logging.getLogger("webscraper")
        
        # Garantir que o diretório de saída exista
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.logger.info(f"Diretório de saída criado: {output_dir}")
            
    @abstractmethod
    def export(self, data, filename=None):
        """
        Exporta os dados para o formato específico.
        
        Args:
            data: Dados a serem exportados
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo exportado
        """
        pass
