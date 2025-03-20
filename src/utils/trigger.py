"""
Módulo de gatilhos para automação de scraping.

Este módulo gerencia a criação e execução de gatilhos programados 
para tarefas de web scraping.
"""

import logging
import datetime
import time
from typing import Callable, Optional, Dict, Any

logger = logging.getLogger(__name__)

def setup_trigger(
    function: Callable,
    interval: int = 3600,  # 1 hora por padrão
    start_time: Optional[datetime.time] = None,
    params: Optional[Dict[str, Any]] = None
) -> Callable:
    """
    Configura um gatilho para executar uma função em intervalos regulares.
    
    Args:
        function: A função que será executada pelo gatilho
        interval: Intervalo em segundos entre execuções
        start_time: Hora de início opcional (formato datetime.time)
        params: Parâmetros opcionais para passar para a função
        
    Returns:
        Uma função wrapper que pode ser usada para iniciar o gatilho
    """
    params = params or {}
    
    def _trigger_wrapper():
        logger.info(f"Configurando gatilho para a função {function.__name__}")
        
        # Se foi definido um horário de início, calcular o tempo de espera inicial
        if start_time:
            now = datetime.datetime.now().time()
            target = datetime.datetime.combine(datetime.date.today(), start_time)
            current = datetime.datetime.combine(datetime.date.today(), now)
            
            if target < current:
                # Se o horário alvo já passou hoje, agendar para amanhã
                target = target + datetime.timedelta(days=1)
                
            wait_seconds = (target - current).total_seconds()
            logger.info(f"Aguardando até {start_time} para iniciar (em {wait_seconds} segundos)")
            time.sleep(wait_seconds)
        
        # Loop principal do gatilho
        while True:
            try:
                logger.info(f"Executando função {function.__name__}")
                function(**params)
            except Exception as e:
                logger.error(f"Erro ao executar função {function.__name__}: {e}")
            
            logger.info(f"Próxima execução em {interval} segundos")
            time.sleep(interval)
    
    return _trigger_wrapper

def start_trigger(trigger_func: Callable, daemon: bool = True) -> None:
    """
    Inicia um gatilho em uma thread separada.
    
    Args:
        trigger_func: A função de gatilho retornada por setup_trigger
        daemon: Se True, a thread será executada como daemon
    """
    import threading
    
    thread = threading.Thread(target=trigger_func, daemon=daemon)
    thread.start()
    return thread
