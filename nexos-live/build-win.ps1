# Build NEXOS Live USB image from Windows using WSL
# Requires WSL and une distribution Linux avec live-build installé.

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
    Write-Error "WSL n'est pas installé. Exécutez : wsl --install"
    exit 1
}

$wslProject = wsl wslpath -a "$projectPath" 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($wslProject)) {
    Write-Error "Impossible de convertir le chemin en chemin WSL. Assurez-vous que WSL est installé correctement."
    exit 1
}

Write-Host "Lancement de la construction dans WSL : $wslProject"
wsl -e bash -lc "cd '$wslProject' && chmod +x build.sh && ./build.sh"
