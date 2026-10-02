$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Python = Get-Command py -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command python -ErrorAction SilentlyContinue }
if (-not $Python) { throw "JARVIS: Python 3.11+ is required." }

& $Python.Source -c "import sys; assert sys.version_info >= (3,11), 'JARVIS: Python 3.11+ is required.'; print('JARVIS: using Python', sys.version.split()[0])"

& $Python.Source -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"

New-Item -ItemType Directory -Force data | Out-Null

Write-Host ""
Write-Host "JARVIS installation complete."
Write-Host "Run: .\.venv\Scripts\Activate.ps1; jarvis"
Write-Host "Health/API: http://127.0.0.1:8080"