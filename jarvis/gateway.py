from fastapi import FastAPI
from pydantic import BaseModel, Field
from .agent import JarvisAgent

app=FastAPI(title="JARVIS Agent Runtime",version="0.1.0")
agent=JarvisAgent()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "jarvis-core"
    messages: list[ChatMessage] = Field(min_length=1)
    session_id: str = "default"

@app.get("/health")
async def health(): return {"status":"ok","service":"jarvis"}

@app.post("/v1/chat/completions")
async def chat(req: ChatRequest):
    last=next((m.content for m in reversed(req.messages) if m.role=="user"), "")
    result=await agent.chat(req.session_id,last,req.model)
    return {"id":req.session_id,"object":"chat.completion",
            "model":req.model,
            "choices":[{"index":0,"message":{"role":"assistant","content":result.text},"finish_reason":"stop"}],
            "usage":{"prompt_tokens":result.input_tokens,"completion_tokens":result.output_tokens}}

@app.get("/v1/memory/search")
async def memory_search(q: str, limit: int=20):
    return {"results":agent.episodic.recall(q,limit)}
