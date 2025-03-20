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
- CI/CD automatizado com GitHub Actions
- Fluxo de trabalho Git padronizado (Conventional Commits)

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
├── .github/           # Configurações do GitHub (PR template, workflows)
├── requirements.txt   # Dependências
└── main.py            # Ponto de entrada
```

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

```bash
# Clone o repositório
git clone https://github.com/luccasfzn/advanced-web-scraper.git

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

### Exportação para Excel

O framework inclui um exportador especializado para Excel que cria planilhas formatadas profissionalmente:

```python
from src.exporters.excel_exporter import ExcelExporter

# Inicializa o exportador
exporter = ExcelExporter(
    output_dir="data",
    filename_prefix="meus_dados",
    sheet_name="Resultados",
    include_index=False
)

# Exporta os dados para Excel
filepath = exporter.export(dados_extraidos)
print(f"Dados exportados para: {filepath}")
```

O exportador Excel inclui:
- Formatação profissional com cabeçalhos destacados
- Layout zebrado para melhor visualização
- Ajuste automático de largura das colunas

## Configuração

Edite os arquivos na pasta `config/` para configurar as URLs alvo, seletores CSS, 
campos a serem extraídos e configurações de rede.

## Fluxo de Trabalho de Desenvolvimento

Este projeto segue um fluxo de trabalho padronizado:

1. **Branches**: Use o script para criar branches com nomenclatura padronizada:
   ```powershell
   ./create-branch.ps1 -tipo feat -descricao "nova funcionalidade"
   ```

2. **Commits**: Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: adiciona novo recurso
   fix: corrige bug específico
   docs: atualiza documentação
   ```

3. **Pull Requests**: Envie alterações via Pull Requests seguindo o template

4. **CI/CD**: Automação de testes, linting e documentação via GitHub Actions

Para mais informações, consulte:
- [Convenção de Commits](./COMMIT_CONVENTION.md)
- [Nomenclatura de Branches](./.github/BRANCH_NAMING.md)

## Licença

MIT
