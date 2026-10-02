import asyncio,json,uuid
class Orchestrator:
    def __init__(self,router,store): self.router=router; self.store=store
    async def run_parallel(self,session_id,prompts,model):
        async def one(prompt):
            cid=uuid.uuid4().hex
            self.store.checkpoint(cid,session_id,json.dumps({"status":"started","prompt":prompt}))
            result=await self.router.route("primary",[{"role":"user","content":prompt}],model)
            self.store.checkpoint(cid,session_id,json.dumps({"status":"done","text":result.text}))
            return result.text
        return await asyncio.gather(*(one(p) for p in prompts))
