"""
Exportador para formato JSON.
"""
import os
import json
import logging
from datetime import datetime
from .base_exporter import BaseExporter

class JSONExporter(BaseExporter):
    """Exportador de dados para formato JSON."""
    
    def __init__(self, output_dir="data", filename_prefix="scraper_result"):
        """
        Inicializa o exportador JSON.
        
        Args:
            output_dir: Diretório de saída para os arquivos
            filename_prefix: Prefixo para os nomes dos arquivos
        """
        super().__init__(output_dir, filename_prefix)
        self.logger = logging.getLogger("webscraper")
        
    def export(self, data, filename=None):
        """
        Exporta os dados para JSON.
        
        Args:
            data: Lista de dicionários com os dados a serem exportados
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo exportado
        """
        if not data:
            self.logger.warning("Nenhum dado para exportar para JSON")
            return None
            
        try:
            # Gerar nome do arquivo se não fornecido
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.filename_prefix}_{timestamp}.json"
                
            # Caminho completo para o arquivo
            filepath = os.path.join(self.output_dir, filename)
            
            # Exportar para JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            self.logger.info(f"Dados exportados para JSON: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar para JSON: {str(e)}")
            raise
