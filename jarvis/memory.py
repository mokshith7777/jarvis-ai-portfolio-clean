from __future__ import annotations
from pathlib import Path
import json
from .state import StateStore

DEFAULT_FILES = {
    "SOUL.md": "# JARVIS SOUL\nStable global persona and operating rules.\n",
    "AGENTS.md": "# JARVIS AGENTS\nProject-local operating context.\n",
    "MEMORY.md": "# JARVIS MEMORY\nCurated project facts and active state.\n",
    "USER.md": "# JARVIS USER\nOperator preferences and output conventions.\n",
}

class HotMemory:
    LIMITS = {"MEMORY.md": 2200, "USER.md": 1375}

    def __init__(self, root: str = ".jarvis/memory"):
        self.root=Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        for name, content in DEFAULT_FILES.items():
            p=self.root/name
            if not p.exists(): p.write_text(content, encoding="utf-8")

    def read(self, name: str) -> str:
        return (self.root/name).read_text(encoding="utf-8")

    def write(self, name: str, content: str):
        if name in self.LIMITS and len(content) > self.LIMITS[name]:
            raise ValueError(f"{name} exceeds curated character limit")
        (self.root/name).write_text(content, encoding="utf-8")

    def snapshot(self, cwd: str | None = None) -> str:
        names=["SOUL.md","AGENTS.md","MEMORY.md","USER.md"]
        if cwd:
            local=Path(cwd)/"AGENTS.md"
            if local.exists(): names=["SOUL.md","MEMORY.md","USER.md"]
        return "\n\n".join(f"## {n}\n{self.read(n)}" for n in names if (self.root/n).exists())

class EpisodicMemory:
    def __init__(self, store: StateStore): self.store=store
    def recall(self, query: str, limit: int=20): return self.store.search_messages(query, limit)
