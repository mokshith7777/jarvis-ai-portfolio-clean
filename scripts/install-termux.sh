#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

pkg update -y
pkg install -y python git

python - <<'PY'
import sys
if sys.version_info < (3, 11):
    raise SystemExit("JARVIS: Python 3.11+ is required.")
print("JARVIS: Python", sys.version.split()[0])
PY

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
mkdir -p data

echo
echo "JARVIS is installed in Termux."
echo "Run: source .venv/bin/activate && jarvis"