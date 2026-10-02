#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"

command -v "$PYTHON_BIN" >/dev/null 2>&1 || {
  echo "JARVIS: Python 3.11+ is required."
  exit 1
}

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 11):
    raise SystemExit("JARVIS: Python 3.11+ is required.")
print(f"JARVIS: using Python {sys.version.split()[0]}")
PY

"$PYTHON_BIN" -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

mkdir -p data
printf '\nJARVIS installation complete.\n'
printf 'Run:  source .venv/bin/activate && jarvis\n'
printf 'Health/API: http://127.0.0.1:8080\n'