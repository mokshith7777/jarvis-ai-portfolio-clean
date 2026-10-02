# JARVIS Agent

A JARVIS-branded autonomous-agent runtime designed to reproduce the documented Hermes Agent capability surface while replacing the product identity, CLI, configuration namespace, commands, prompt branding, and visual identity with JARVIS.

## Identity

| Source surface | JARVIS surface |
|---|---|
| Hermes Agent | JARVIS Agent |
| `hermes` executable | `jarvis` executable |
| `hermes-agent` package identity | `jarvis-agent-runtime` |
| `~/.hermes` namespace | `~/.jarvis` |
| `HERMES_*` variables | `JARVIS_*` |
| Hermes banner/prompt | JARVIS banner/prompt |
| Hermes command registry | JARVIS command registry |
| Hermes slash commands | JARVIS slash commands |

The upstream project is MIT licensed. This derivative keeps the required attribution/licensing obligations while replacing the product identity with JARVIS.

## CLI

```bash
jarvis
jarvis --version
jarvis chat -q "Hello"
jarvis model
jarvis setup
jarvis gateway
jarvis config
jarvis profile
jarvis tools
jarvis skills
jarvis doctor
jarvis update
jarvis --tui
```

Interactive commands:

```text
/help
/new
/reset
/model
/personality
/retry
/undo
/compress
/usage
/insights
/skills
/stop
/platforms
/status
/save
/profile
/tools
/gateway
/update
/quit
```

## Runtime

- Persistent SQLite WAL + FTS5 memory
- Stable hot-memory prompt prefix
- Dual-layer context-compression configuration
- Provider abstraction and auxiliary routing
- Parallel subagent orchestration with checkpoints
- Skill storage and validation
- OpenAI-compatible API
- Programmatic execution guardrails
- Hardened Docker defaults
- CI tests

## Scope

The current repository contains the JARVIS runtime foundation and the compatibility surface. Full feature parity requires porting the remaining upstream modules, including the complete TUI, provider catalog, messaging adapters, browser/CDP stack, MCP integration, cron, ACP, richer skills lifecycle, and production sandbox/RPC implementation.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
jarvis
pytest -q
```

API: `http://127.0.0.1:8080`
