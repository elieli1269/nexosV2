Param(
  [string]$Repo = 'nexosnexaibuild'
)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Error "GitHub CLI 'gh' introuvable. Installez-la : https://cli.github.com/"
  exit 1
}

if (-not (Test-Path .git)) { git init }

git add .
try { git commit -m "Initial commit: NEXOS + backend + CI" } catch { }

# Create and push
gh repo create $Repo --public --source=. --remote=origin --push

Write-Output "Repository created and pushed (if permitted)."