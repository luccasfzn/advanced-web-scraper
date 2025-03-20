"""
Testes básicos para o web scraper.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config_manager import ConfigManager
from src.utils.user_agents import UserAgentManager
from src.exporters.csv_exporter import CSVExporter
from src.exporters.json_exporter import JSONExporter

class TestConfigManager(unittest.TestCase):
    """Testes para o gerenciador de configuração."""
    
    def test_default_config(self):
        """Testa se a configuração padrão é carregada corretamente."""
        config_manager = ConfigManager()
        config = config_manager.get_config()
        
        self.assertIn("urls", config)
        self.assertIn("scraper_settings", config)
        self.assertIn("export_settings", config)
        
    @patch('builtins.open', new_callable=unittest.mock.mock_open, 
           read_data='{"urls": ["https://example.com"], "scraper_settings": {"max_workers": 2}}')
    @patch('json.load')
    def test_load_config(self, mock_json_load, mock_open):
        """Testa o carregamento de configuração de um arquivo."""
        mock_json_load.return_value = {
            "urls": ["https://example.com"],
            "scraper_settings": {"max_workers": 2}
        }
        
        with patch('os.path.exists', return_value=True):
            config_manager = ConfigManager("dummy_path.json")
            mock_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')

class TestUserAgentManager(unittest.TestCase):
    """Testes para o gerenciador de user-agents."""
    
    def test_get_random_user_agent(self):
        """Testa se um user-agent aleatório é retornado."""
        ua_manager = UserAgentManager(use_fake_ua=False)
        ua = ua_manager.get_random_user_agent()
        
        self.assertIsInstance(ua, str)
        self.assertGreater(len(ua), 10)  # User agent deve ter um tamanho razoável
        
    def test_get_header(self):
        """Testa se os headers são gerados corretamente."""
        ua_manager = UserAgentManager(use_fake_ua=False)
        headers = ua_manager.get_header()
        
        self.assertIn('User-Agent', headers)
        self.assertIn('Accept', headers)
        self.assertIn('Accept-Language', headers)
        
        # Testa adição de headers customizados
        custom_headers = {'X-Custom': 'Value'}
        headers = ua_manager.get_header(custom_headers)
        self.assertEqual(headers['X-Custom'], 'Value')

class TestExporters(unittest.TestCase):
    """Testes para os exportadores de dados."""
    
    @patch('pandas.DataFrame.to_csv')
    @patch('os.makedirs')
    def test_csv_exporter(self, mock_makedirs, mock_to_csv):
        """Testa o exportador CSV."""
        data = [{'field1': 'value1', 'field2': 'value2'}]
        exporter = CSVExporter(output_dir="test_dir", filename_prefix="test")
        
        with patch('os.path.exists', return_value=False):
            exporter.export(data, "test_output.csv")
            
        mock_makedirs.assert_called_once()
        mock_to_csv.assert_called_once()
    
    @patch('json.dump')
    @patch('os.makedirs')
    def test_json_exporter(self, mock_makedirs, mock_json_dump):
        """Testa o exportador JSON."""
        data = [{'field1': 'value1', 'field2': 'value2'}]
        exporter = JSONExporter(output_dir="test_dir", filename_prefix="test")
        
        with patch('os.path.exists', return_value=False):
            with patch('builtins.open', unittest.mock.mock_open()) as mock_open:
                exporter.export(data, "test_output.json")
                
        mock_makedirs.assert_called_once()
        mock_json_dump.assert_called_once()

if __name__ == '__main__':
    unittest.main()
