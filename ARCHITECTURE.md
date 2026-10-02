# JARVIS architecture

This implementation translates the uploaded Hermes-to-JARVIS blueprint into a clean modular foundation.

## Core loop

1. Gateway normalizes input.
2. Stable hot-memory files are loaded as a prompt prefix.
3. SQLite WAL stores exact session history and a persistent usage anchor.
4. Context pressure is checked before the provider call.
5. Provider routing separates primary reasoning from auxiliary work.
6. Tool execution is bounded by approval, timeout and call-count controls.
7. Subagent work is isolated logically and checkpointed after each unit.
8. Skills provide reusable procedural memory.

## Compression

The blueprint calls for two layers: gateway hygiene around 85% and an agent-loop compressor around 50%, with a 75% floor for smaller windows, a 20% target tail and protection for the latest 20 messages. The runtime exposes those values as configuration.

## Memory

Hot memory is curated in SOUL.md, AGENTS.md, MEMORY.md and USER.md. Episodic history remains exact in SQLite FTS5 rather than relying exclusively on semantic summaries.

## Routing

Provider transport is behind a small interface so OpenAI-compatible endpoints, local models and other providers can be plugged in without changing orchestration logic.

## Security

The source blueprint treats the host OS as the real security boundary. This foundation therefore uses non-root Docker defaults, dropped capabilities, no-new-privileges and explicit execution gates. The code executor is intentionally not marketed as a perfect sandbox. Production execution should move to a dedicated hardened worker.

## Scope

Browser automation, MCP servers, production-grade Unix-socket RPC, model-specific compaction, encrypted credential storage and self-evolution PR automation are extension points for later releases.
