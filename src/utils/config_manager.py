"""
Gerenciador de configuração para o web scraper.
"""
import os
import json
import logging
from jsonschema import validate
from dotenv import load_dotenv

class ConfigManager:
    """Carrega e valida configurações para o scraper."""
    
    # Schema para validação do arquivo de configuração
    CONFIG_SCHEMA = {
        "type": "object",
        "required": ["urls", "scraper_settings"],
        "properties": {
            "urls": {
                "type": "array",
                "items": {"type": "string"}
            },
            "scraper_settings": {
                "type": "object",
                "properties": {
                    "max_workers": {"type": "integer", "minimum": 1},
                    "min_delay": {"type": "number", "minimum": 0},
                    "max_delay": {"type": "number", "minimum": 0},
                    "timeout": {"type": "number", "minimum": 0},
                    "retries": {"type": "integer", "minimum": 0},
                    "selectors": {"type": "object"},
                    "use_selenium": {"type": "boolean"},
                    "headless": {"type": "boolean"},
                    "proxy": {"type": "string"}
                }
            },
            "export_settings": {
                "type": "object",
                "properties": {
                    "formats": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["csv", "json", "excel"]}
                    },
                    "output_dir": {"type": "string"},
                    "filename_prefix": {"type": "string"}
                }
            },
            "categories": {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    }
    
    def __init__(self, config_path=None, env_file=None):
        """
        Inicializa o gerenciador de configuração.
        
        Args:
            config_path: Caminho para o arquivo de configuração
            env_file: Caminho para o arquivo .env
        """
        self.logger = logging.getLogger("webscraper")
        
        # Carregar variáveis de ambiente se o arquivo for especificado
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)
            self.logger.info(f"Variáveis de ambiente carregadas de: {env_file}")
            
        # Inicializar configuração padrão
        self.config = {
            "urls": [],
            "scraper_settings": {
                "max_workers": 4,
                "min_delay": 1.0,
                "max_delay": 3.0,
                "timeout": 30,
                "retries": 3,
                "use_selenium": False,
                "headless": True
            },
            "export_settings": {
                "formats": ["csv"],
                "output_dir": "data",
                "filename_prefix": "scraper_result"
            }
        }
        
        # Carregar configuração se o arquivo for especificado
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def load_config(self, config_path):
        """
        Carrega configurações a partir de um arquivo JSON.
        
        Args:
            config_path: Caminho para o arquivo de configuração
            
        Returns:
            Dicionário com as configurações carregadas
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                
            # Validar configuração
            validate(instance=loaded_config, schema=self.CONFIG_SCHEMA)
            
            # Atualizar configuração padrão com a configuração carregada
            self._update_config(loaded_config)
            
            self.logger.info(f"Configuração carregada com sucesso de: {config_path}")
            return self.config
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração de {config_path}: {str(e)}")
            raise
    
    def _update_config(self, new_config):
        """
        Atualiza a configuração atual com novos valores.
        
        Args:
            new_config: Novos valores de configuração
        """
        # Função recursiva para atualizar dicionários aninhados
        def update_nested_dict(d, u):
            for k, v in u.items():
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    update_nested_dict(d[k], v)
                else:
                    d[k] = v
        
        update_nested_dict(self.config, new_config)
    
    def get_config(self):
        """Retorna a configuração atual."""
        return self.config
    
    def save_config(self, config_path):
        """
        Salva a configuração atual em um arquivo JSON.
        
        Args:
            config_path: Caminho para salvar o arquivo de configuração
        """
        try:
            # Garantir que o diretório exista
            os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
                
            self.logger.info(f"Configuração salva com sucesso em: {config_path}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar configuração em {config_path}: {str(e)}")
            raise
