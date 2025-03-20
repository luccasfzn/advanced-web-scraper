module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',    // Nova funcionalidade
        'fix',     // Correção de bug
        'docs',    // Documentação
        'style',   // Alterações de formatação que não afetam o código
        'refactor',// Refatoração de código
        'perf',    // Melhorias de performance
        'test',    // Adicionando testes
        'chore',   // Alterações em ferramentas, configurações, etc.
        'ci',      // Alterações no pipeline de CI
        'build',   // Alterações no sistema de build
        'revert'   // Reverte para um commit anterior
      ]
    ],
    'type-case': [2, 'always', 'lower'],
    'subject-case': [0], // Desabilitado para permitir flexibilidade
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 72]
  }
};
