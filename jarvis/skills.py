from __future__ import annotations
from pathlib import Path
import re, time, yaml

class SkillStore:
    def __init__(self, root=".jarvis/skills"):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def save(self,name: str, description: str, body: str):
        if len(body.encode()) > 15_000: raise ValueError("skill exceeds 15 KB")
        if len(description) > 500: raise ValueError("tool description exceeds 500 characters")
        safe=re.sub(r"[^a-zA-Z0-9_-]","-",name).strip("-").lower()
        text=f"---\nname: {safe}\ndescription: {description}\n---\n\n{body}\n"
        (self.root/f"{safe}.md").write_text(text,encoding="utf-8")
        return safe
    def list(self):
        return sorted(p.name for p in self.root.glob("*.md"))
    def read(self,name):
        return (self.root/name).read_text(encoding="utf-8")

class SkillCurator:
    def __init__(self, store: SkillStore): self.store=store
    def archive_unused(self, max_age_days=90):
        # Telemetry integration can be added without changing the skill format.
        return []
