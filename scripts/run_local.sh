#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"
if [ ! -d .venv ]; then "$PYTHON_BIN" -m venv .venv; fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export DEBUG="${DEBUG:-true}"
export SECRET_KEY="${SECRET_KEY:-local-dev-secret-change-me}"
export ALLOWED_HOSTS="${ALLOWED_HOSTS:-localhost,127.0.0.1,0.0.0.0,10.0.2.2}"
python manage.py migrate
python manage.py seed_demo
python manage.py check
exec python manage.py runserver 0.0.0.0:8000
