# Advanced Web Scraper

Um framework robusto e escalável para web scraping, desenvolvido para lidar com diversos cenários de extração de dados.

## Características

- Arquitetura orientada a objetos para código organizado e manutenível
- Processamento paralelo para scraping eficiente
- Sistema de logging avançado
- Suporte a múltiplos formatos de exportação (CSV, JSON, Excel)
- Configuração baseada em arquivos externos
- Rotação de User-Agents e delays aleatórios para evitar bloqueios
- Sistema de retry para URLs problemáticas
- Proxy rotation (opcional)

## Estrutura do Projeto

```
advanced-web-scraper/
├── config/            # Arquivos de configuração
├── data/              # Dados exportados
├── logs/              # Arquivos de log
├── src/               # Código-fonte
│   ├── scrapers/      # Implementações de scrapers específicos
│   ├── exporters/     # Módulos para exportação de dados
│   └── utils/         # Utilitários e helpers
├── requirements.txt   # Dependências
└── main.py            # Ponto de entrada
```

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>

# Navegue até o diretório
cd advanced-web-scraper

# Instale as dependências
pip install -r requirements.txt
```

## Uso

```python
# Exemplo básico de uso
python main.py --config=config/example.json
```

## Configuração

Edite os arquivos na pasta `config/` para configurar as URLs alvo, seletores CSS, 
campos a serem extraídos e configurações de rede.

## Licença

MIT
