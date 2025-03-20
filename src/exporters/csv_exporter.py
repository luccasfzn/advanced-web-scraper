"""
Exportador para formato CSV.
"""
import os
import logging
import pandas as pd
from datetime import datetime
from .base_exporter import BaseExporter

class CSVExporter(BaseExporter):
    """Exportador de dados para formato CSV."""
    
    def __init__(self, output_dir="data", filename_prefix="scraper_result"):
        """
        Inicializa o exportador CSV.
        
        Args:
            output_dir: Diretório de saída para os arquivos
            filename_prefix: Prefixo para os nomes dos arquivos
        """
        super().__init__(output_dir, filename_prefix)
        self.logger = logging.getLogger("webscraper")
        
    def export(self, data, filename=None):
        """
        Exporta os dados para CSV.
        
        Args:
            data: Lista de dicionários com os dados a serem exportados
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo exportado
        """
        if not data:
            self.logger.warning("Nenhum dado para exportar para CSV")
            return None
            
        try:
            # Criar DataFrame
            df = pd.DataFrame(data)
            
            # Gerar nome do arquivo se não fornecido
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.filename_prefix}_{timestamp}.csv"
                
            # Caminho completo para o arquivo
            filepath = os.path.join(self.output_dir, filename)
            
            # Exportar para CSV com codificação adequada
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            self.logger.info(f"Dados exportados para CSV: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar para CSV: {str(e)}")
            raise
