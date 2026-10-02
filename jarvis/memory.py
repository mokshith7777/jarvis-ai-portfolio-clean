from pathlib import Path
from .state import StateStore
DEFAULT_FILES={"SOUL.md":"# JARVIS SOUL\nStable global persona and operating rules.\n","AGENTS.md":"# JARVIS AGENTS\nProject-local operating context.\n","MEMORY.md":"# JARVIS MEMORY\nCurated project facts and active state.\n","USER.md":"# JARVIS USER\nOperator preferences and output conventions.\n"}
class HotMemory:
    LIMITS={"MEMORY.md":2200,"USER.md":1375}
    def __init__(self,root=".jarvis/memory"):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
        for n,c in DEFAULT_FILES.items():
            p=self.root/n
            if not p.exists(): p.write_text(c,encoding="utf-8")
    def read(self,name): return (self.root/name).read_text(encoding="utf-8")
    def write(self,name,content):
        if name in self.LIMITS and len(content)>self.LIMITS[name]: raise ValueError(f"{name} exceeds curated character limit")
        (self.root/name).write_text(content,encoding="utf-8")
    def snapshot(self,cwd=None): return "\n\n".join(f"## {n}\n{self.read(n)}" for n in DEFAULT_FILES)
class EpisodicMemory:
    def __init__(self,store:StateStore): self.store=store
    def recall(self,query,limit=20): return self.store.search_messages(query,limit)
