$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$gitHooks = Join-Path $root ".git/hooks"
New-Item -ItemType Directory -Force -Path $gitHooks | Out-Null
Copy-Item (Join-Path $PSScriptRoot "pre-push") (Join-Path $gitHooks "pre-push") -Force
Write-Host "Hook pre-push instalado en $gitHooks"
