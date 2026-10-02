from dataclasses import dataclass
@dataclass
class CompressionResult: compressed: bool; summary: str|None; kept: int
class ContextManager:
    def __init__(self,store,max_tokens,threshold=.50,target_ratio=.20,protect_last_n=20):
        self.store=store; self.max_tokens=max_tokens; self.threshold=threshold; self.target_ratio=target_ratio; self.protect_last_n=protect_last_n
    def estimate(self,messages): return sum(max(1,len(m["content"])//4) for m in messages)
    def needs_compression(self,messages):
        floor=.75 if self.max_tokens<512_000 else self.threshold
        return self.estimate(messages)>self.max_tokens*max(self.threshold,floor)
    def compress(self,sid,messages):
        if not self.needs_compression(messages) or len(messages)<=self.protect_last_n: return CompressionResult(False,None,len(messages))
        old=messages[:-self.protect_last_n]
        summary="Compressed historical context:\n"+"\n".join(f"- {m['role']}: {m['content'][:500]}" for m in old[-40:])
        self.store.add_message(sid,"system",summary,max(1,len(summary)//4))
        return CompressionResult(True,summary,self.protect_last_n)
