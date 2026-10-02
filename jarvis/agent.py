from __future__ import annotations
from .config import settings
from .state import StateStore
from .memory import HotMemory, EpisodicMemory
from .context import ContextManager
from .providers import MockProvider, ProviderRouter
from .orchestrator import Orchestrator

class JarvisAgent:
    def __init__(self):
        settings.ensure_dirs()
        self.store=StateStore(settings.db)
        self.hot=HotMemory()
        self.episodic=EpisodicMemory(self.store)
        self.context=ContextManager(self.store, settings.max_context_tokens,
            settings.compression_threshold, settings.compression_target_ratio,
            settings.protect_last_n)
        self.router=ProviderRouter(MockProvider(),MockProvider())
        self.orchestrator=Orchestrator(self.router,self.store)

    async def chat(self, session_id: str, text: str, model="jarvis-core"):
        self.store.upsert_session(session_id,"default",model)
        self.store.add_message(session_id,"user",text,max(1,len(text)//4))
        messages=self.store.recent_messages(session_id,200)
        self.context.compress(session_id,messages)
        prompt=[{"role":"system","content":self.hot.snapshot()}]
        prompt += [{"role":m["role"],"content":m["content"]} for m in self.store.recent_messages(session_id,200)]
        result=await self.router.route("primary",prompt,model)
        self.store.add_message(session_id,"assistant",result.text,result.output_tokens or max(1,len(result.text)//4))
        self.store.set_anchor(session_id,result.input_tokens+result.output_tokens)
        return result
