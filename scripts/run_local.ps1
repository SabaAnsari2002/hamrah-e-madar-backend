$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
if (-not (Test-Path ".venv")) { py -3 -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\pip.exe install -r requirements.txt
$env:DEBUG = if ($env:DEBUG) { $env:DEBUG } else { "true" }
$env:SECRET_KEY = if ($env:SECRET_KEY) { $env:SECRET_KEY } else { "local-dev-secret-change-me" }
$env:ALLOWED_HOSTS = if ($env:ALLOWED_HOSTS) { $env:ALLOWED_HOSTS } else { "localhost,127.0.0.1,0.0.0.0,10.0.2.2" }
& .\.venv\Scripts\python.exe manage.py migrate
& .\.venv\Scripts\python.exe manage.py seed_demo
& .\.venv\Scripts\python.exe manage.py check
& .\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
