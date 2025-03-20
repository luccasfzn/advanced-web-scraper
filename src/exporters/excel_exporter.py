"""
Exportador para formato Excel.
"""
import os
import pandas as pd
import logging
from datetime import datetime
from src.exporters.base_exporter import BaseExporter

class ExcelExporter(BaseExporter):
    """
    Classe para exportar dados para o formato Excel (.xlsx).
    
    Herda da classe base BaseExporter e implementa a lógica
    específica para exportação de dados no formato Excel.
    """
    
    def __init__(self, output_dir="data", filename_prefix="scraper_result", 
                 sheet_name="Dados", include_index=False):
        """
        Inicializa o exportador Excel.
        
        Args:
            output_dir: Diretório de saída para os arquivos
            filename_prefix: Prefixo para os nomes dos arquivos
            sheet_name: Nome da planilha Excel
            include_index: Se deve incluir o índice do DataFrame no Excel
        """
        super().__init__(output_dir, filename_prefix)
        self.sheet_name = sheet_name
        self.include_index = include_index
        self.logger = logging.getLogger("webscraper")
        
    def export(self, data, filename=None):
        """
        Exporta os dados para o formato Excel.
        
        Args:
            data: Dados a serem exportados (lista de dicionários)
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo exportado
        """
        if not data:
            self.logger.warning("Nenhum dado para exportar.")
            return None
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.filename_prefix}_{timestamp}.xlsx"
            
        # Garantir extensão .xlsx
        if not filename.endswith('.xlsx'):
            filename = f"{filename}.xlsx"
            
        # Caminho completo do arquivo
        file_path = os.path.join(self.output_dir, filename)
        
        # Criação do DataFrame a partir dos dados
        df = pd.DataFrame(data)
        
        # Configurações específicas do Excel
        excel_writer = pd.ExcelWriter(
            file_path, 
            engine='xlsxwriter'
        )
        
        # Exportação para Excel com formatação melhorada
        df.to_excel(
            excel_writer, 
            sheet_name=self.sheet_name,
            index=self.include_index
        )
        
        # Ajustar colunas (autofit)
        workbook = excel_writer.book
        worksheet = excel_writer.sheets[self.sheet_name]
        
        # Formato de cabeçalho
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Aplicar formato ao cabeçalho
        for col_num, value in enumerate(df.columns.values):
            if self.include_index:
                col_num += 1  # Ajuste para considerar a coluna de índice
            worksheet.write(0, col_num, value, header_format)
            # Ajuste automático da largura da coluna
            max_len = max(
                df[value].astype(str).map(len).max(),
                len(str(value))
            ) + 2
            worksheet.set_column(col_num, col_num, max_len)
        
        # Aplicar formato zebrado para as linhas
        zebra_format = workbook.add_format({'bg_color': '#F2F2F2'})
        for row_num in range(1, len(df) + 1, 2):
            worksheet.set_row(row_num, None, zebra_format)
            
        # Salvar o arquivo
        excel_writer.close()
        
        self.logger.info(f"Dados exportados para Excel: {file_path}")
        return file_path
