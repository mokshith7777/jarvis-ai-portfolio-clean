# JARVIS Installation

JARVIS is a Python 3.11+ application. The repository provides installation paths for Linux, macOS, Windows, Android/Termux, and Docker.

## Linux / macOS

From the repository root:

```bash
bash scripts/install.sh
source .venv/bin/activate
jarvis
```

## Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
.\.venv\Scripts\Activate.ps1
jarvis
```

## Android / Termux

Clone the repository inside Termux, then:

```bash
bash scripts/install-termux.sh
source .venv/bin/activate
jarvis
```

The Termux path is intentionally kept Python-only so it can also run inside a proot Ubuntu environment.

## Docker

```bash
docker compose up --build
```

The API is exposed on `127.0.0.1:8080` by default.

## Direct Python installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
jarvis
```

## Configuration

Copy `.env.example` to `.env`. Settings use the `JARVIS_` environment prefix.

Examples:

```text
JARVIS_HOST=127.0.0.1
JARVIS_PORT=8080
JARVIS_PRIMARY_PROVIDER=mock
JARVIS_AUX_PROVIDER=mock
```

The default provider is `mock`, so installation does not require an API key just to start the runtime.

## Verification

Run:

```bash
python -m pytest -q
python scripts/smoke_test.py
```

CI also verifies Linux, macOS, and Windows across supported Python versions.

## Important scope note

The repository currently contains the JARVIS runtime foundation and an upstream-sync mechanism. Full Hermes behavioral parity is a separate milestone from installation. The installer makes the current JARVIS runtime reproducibly installable; it does not claim that every upstream Hermes command has already been reimplemented.