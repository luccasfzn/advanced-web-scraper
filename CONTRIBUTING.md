# Contribuindo com o Advanced Web Scraper

Obrigado pelo interesse em contribuir com o projeto! Aqui estão algumas diretrizes para ajudar.

## Fluxo de trabalho

Este projeto utiliza automação via MCP (Minimum Continuous Pipeline) para facilitar o fluxo de desenvolvimento:

- Commits automáticos são programados diariamente à meia-noite
- Alterações em arquivos Python, JavaScript, HTML e CSS acionam automações
- Documentação em markdown é gerada automaticamente
- Notificações são enviadas após eventos importantes

## Configuração do ambiente

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Copie o arquivo `.env.example` para `.env` e configure conforme necessário

## Padrões de código

- Utilize PEP 8 para código Python
- Documente funções e classes usando docstrings no formato do Google
- Mantenha a cobertura de testes acima de 80%

## Enviando mudanças

1. Crie um branch para a sua feature: `git checkout -b feature/nome-da-feature`
2. Faça commit das mudanças: `git commit -am 'Adiciona nova feature'`
3. Envie para o branch: `git push origin feature/nome-da-feature`
4. Envie um Pull Request

## Estrutura do projeto

- `src/`: Código-fonte principal
- `config/`: Arquivos de configuração
- `data/`: Diretório para dados exportados (ignorado pelo git)
- `logs/`: Logs de execução (ignorado pelo git)

## Configuração de scrapers

Para adicionar suporte a novos sites, crie arquivos de configuração na pasta `config/` seguindo o padrão dos existentes.
