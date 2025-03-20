"""
Utilitário para processamento concorrente de tarefas de scraping.
"""
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

class ScraperConcurrencyManager:
    """Gerencia o processamento concorrente de tarefas de scraping."""
    
    def __init__(self, 
                max_workers=5, 
                min_delay=1.0, 
                max_delay=5.0, 
                fixed_delay=None):
        """
        Inicializa o gerenciador de concorrência.
        
        Args:
            max_workers: Número máximo de workers para processamento paralelo
            min_delay: Delay mínimo entre requisições (segundos)
            max_delay: Delay máximo entre requisições (segundos)
            fixed_delay: Se definido, usa um delay fixo ao invés de aleatório
        """
        self.max_workers = max_workers
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.fixed_delay = fixed_delay
        self.logger = logging.getLogger("webscraper")
        
    def process_batch(self, urls, process_func, desc="Processando URLs"):
        """
        Processa um lote de URLs em paralelo com delays entre requisições.
        
        Args:
            urls: Lista de URLs para processar
            process_func: Função para processar cada URL
            desc: Descrição para a barra de progresso
            
        Returns:
            Lista com os resultados do processamento
        """
        results = []
        
        self.logger.info(f"Iniciando processamento paralelo de {len(urls)} URLs com {self.max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submeter todas as tarefas
            future_to_url = {executor.submit(self._process_with_delay, process_func, url): url for url in urls}
            
            # Processar resultados conforme forem concluídos
            with tqdm(total=len(urls), desc=desc) as progress:
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        result = future.result()
                        results.append(result)
                        self.logger.debug(f"URL processada com sucesso: {url}")
                    except Exception as e:
                        self.logger.error(f"Erro ao processar URL {url}: {str(e)}")
                        # Adicionar resultado de erro para manter o tamanho consistente da lista
                        results.append({"url": url, "error": str(e), "status": "error"})
                    finally:
                        progress.update(1)
        
        return results
    
    def _process_with_delay(self, process_func, url):
        """
        Processa uma URL e aplica um delay após o processamento.
        
        Args:
            process_func: Função para processar a URL
            url: URL para processar
            
        Returns:
            Resultado do processamento
        """
        try:
            result = process_func(url)
            
            # Aplicar delay após o processamento
            if self.fixed_delay is not None:
                delay = self.fixed_delay
            else:
                delay = random.uniform(self.min_delay, self.max_delay)
                
            self.logger.debug(f"Aguardando {delay:.2f}s após processar {url}")
            time.sleep(delay)
            
            return result
        except Exception as e:
            self.logger.error(f"Erro durante o processamento de {url}: {str(e)}")
            raise
