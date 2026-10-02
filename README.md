# JARVIS Agent Runtime

A modular, open-source agent runtime inspired by the architecture described in the attached Hermes-to-JARVIS blueprint.

## Architecture implemented

- Stable system prompt and profile snapshots
- Dual-layer context compression with persistent usage anchors
- SQLite WAL + FTS5 episodic memory
- Hot memory files: `SOUL.md`, `AGENTS.md`, `MEMORY.md`, `USER.md`
- Programmatic tool execution through an RPC-style dispatcher
- Configurable execution timeout and RPC-call limits
- Provider abstraction with role-based auxiliary-model routing
- Skill storage, validation, and usage telemetry
- Parallel subagent orchestration with checkpoints
- OpenAI-compatible FastAPI gateway
- Approval gates and catastrophic-operation blocking
- Docker hardening defaults and CI tests

## Status

This is the first runnable foundation. Provider adapters, browser/MCP integrations, and model-specific connectors are intentionally isolated behind interfaces so they can be added without changing the core agent loop.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
python -m jarvis
```

API: `http://127.0.0.1:8080`

Run tests:

```bash
pytest
```

Run with Docker:

```bash
docker compose up --build
```

## Security

The default approval mode is `smart`. Secrets are never loaded into prompts by the runtime. Code execution is isolated as a child process and is deliberately conservative; production deployments should place the worker inside a hardened container or stronger OS sandbox.

This repository is a clean reimplementation of architectural ideas. It does not copy proprietary source code or branding from another project.


## Installation across platforms

See [INSTALL.md](INSTALL.md) for Linux, macOS, Windows, Android/Termux, and Docker installation. Cross-platform CI runs on every push and pull request.
