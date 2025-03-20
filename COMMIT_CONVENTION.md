# Convenção de Commits

Este projeto utiliza a convenção de Conventional Commits para manter um histórico de commits padronizado e facilitar a automação de versões e changelogs.

## Estrutura de um Commit Convencional

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé(s) opcional(is)]
```

## Tipos de Commits

Os principais tipos de commits que utilizamos são:

| Tipo     | Descrição                                                        |
|----------|-----------------------------------------------------------------|
| `feat`   | Uma nova funcionalidade ou recurso                              |
| `fix`    | Correção de bugs ou erros                                       |
| `docs`   | Alterações apenas na documentação                               |
| `style`  | Alterações que não afetam o código (formatação, espaços, etc.)  |
| `refactor` | Alteração de código que não corrige bug nem adiciona recurso  |
| `perf`   | Alteração de código que melhora performance                     |
| `test`   | Adicionando novos testes ou corrigindo testes existentes        |
| `chore`  | Alterações no processo de build, ferramentas, config, etc.      |
| `ci`     | Alterações em arquivos de CI/CD                                |
| `build`  | Alterações que afetam o sistema de build ou dependências        |
| `revert` | Reverte um commit anterior                                      |

## Exemplos

```
feat(scraper): adiciona suporte para detecção automática de seletores

fix(exporters): corrige codificação UTF-8 no CSV

docs: atualiza documentação da API

style: formata código com Black

refactor(selenium): melhora estrutura do módulo de tratamento de erros

test: adiciona testes para o módulo de concorrência

chore: atualiza dependências

ci: configura github actions para testes em múltiplos ambientes
```

## Ferramentas para Auxiliar na Escrita de Commits

1. **Commitizen**: Use `npm run commit` para uma interface interativa guiada
2. **Husky + Commitlint**: Hooks de git que validam seus commits automaticamente

## Automação MCP e Integração com Commits Convencionais

O MCP (Minimum Continuous Pipeline) configurado no Windsurf usa essa semântica para:

1. Gerar automaticamente CHANGELOG.md baseado nos commits
2. Incrementar versões automaticamente:
   - `fix` → incrementa a versão de patch (1.0.0 → 1.0.1)
   - `feat` → incrementa a versão minor (1.0.0 → 1.1.0)
   - `feat` com `BREAKING CHANGE` no corpo → incrementa a versão major (1.0.0 → 2.0.0)

3. Acionar workflows específicos baseados no tipo:
   - `docs` → atualiza automaticamente documentação
   - `feat`, `fix` → executa testes completos e deploy
   - Outros tipos → executa linting e testes básicos

## Fluxo de Trabalho Recomendado

1. Faça suas alterações no código
2. Execute `git add .` para adicionar suas mudanças
3. Use `npm run commit` para um commit guiado que segue a convenção
4. Caso prefira commits manuais, lembre-se de seguir o formato:
   ```
   <tipo>(<escopo opcional>): <descrição>
   ```
5. O hook de commit verificará se seu commit segue a convenção

## Categorização Automática

A convenção de commits permite categorizar automaticamente as mudanças:

- **Novos recursos**: commits com `feat:`
- **Correções**: commits com `fix:`
- **Melhorias na documentação**: commits com `docs:`
- **Melhorias técnicas**: commits com `refactor:`, `perf:`, `style:`
