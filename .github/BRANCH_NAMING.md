# Convenção de Nomenclatura de Branches

Este projeto segue uma convenção de nomenclatura de branches para manter organização e clareza no fluxo de trabalho de desenvolvimento.

## Estrutura de Nomenclatura

```
<tipo>/<descrição>
```

Por exemplo:
- `feat/adiciona-exportacao-excel`
- `fix/corrige-extrator-imagens` 
- `docs/atualiza-readme`

## Tipos de Branches

Os tipos de branches devem corresponder aos tipos de commits da [Conventional Commits](./COMMIT_CONVENTION.md):

| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Alterações em documentação |
| `style` | Alterações que não afetam o código (formatação, etc.) |
| `refactor` | Alterações de código que não corrigem bugs nem adicionam recursos |
| `perf` | Alterações para melhorar performance |
| `test` | Adição ou modificação de testes |
| `chore` | Alterações em ferramentas, scripts, configurações, etc. |
| `ci` | Alterações em arquivos de CI/CD |
| `build` | Alterações no sistema de build ou dependências |

## Fluxo de Trabalho

1. Sempre crie branches a partir da `main` atualizada
2. Use o script `create-branch.ps1` para criar branches facilmente:
   ```powershell
   ./create-branch.ps1 -tipo feat -descricao "adiciona novo recurso"
   ```
3. Faça seus commits seguindo a convenção de Conventional Commits
4. Envie sua branch para o GitHub e crie um Pull Request