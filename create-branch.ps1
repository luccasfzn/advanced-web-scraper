# Script para criar novas branches seguindo a convenção
param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("feat", "fix", "docs", "style", "refactor", "perf", "test", "chore", "ci", "build")]
    [string]$tipo,
    
    [Parameter(Mandatory=$true)]
    [string]$descricao
)

# Formata a descrição removendo espaços e caracteres especiais
$descricaoFormatada = $descricao -replace " ", "-" -replace "[^a-zA-Z0-9\-]", ""

# Cria o nome da branch seguindo a convenção
$branchName = "$tipo/$descricaoFormatada"

# Verifica se há alterações não commitadas
$status = git status --porcelain
if ($status) {
    Write-Host "ATENÇÃO: Existem alterações não commitadas. Commit ou stash antes de criar uma nova branch." -ForegroundColor Yellow
    git status
    exit 1
}

# Atualiza a branch atual
git pull

# Cria e muda para a nova branch
git checkout -b $branchName

Write-Host "Branch '$branchName' criada com sucesso!" -ForegroundColor Green
Write-Host "Para enviar para o GitHub, use: git push -u origin $branchName" -ForegroundColor Cyan
