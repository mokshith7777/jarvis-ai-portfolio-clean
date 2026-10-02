from __future__ import annotations
import asyncio, json, uuid
from dataclasses import dataclass
from .state import StateStore
from .providers import ProviderRouter

@dataclass
class Subtask:
    id: str
    prompt: str
    model: str

class Orchestrator:
    def __init__(self, router: ProviderRouter, store: StateStore):
        self.router=router; self.store=store
    async def run_parallel(self, session_id: str, prompts: list[str], model: str):
        async def one(prompt):
            sid=uuid.uuid4().hex
            self.store.checkpoint(sid, session_id, json.dumps({"status":"started","prompt":prompt}))
            result=await self.router.route("primary",[{"role":"user","content":prompt}],model)
            self.store.checkpoint(sid, session_id, json.dumps({"status":"done","text":result.text}))
            return result.text
        return await asyncio.gather(*(one(p) for p in prompts))
