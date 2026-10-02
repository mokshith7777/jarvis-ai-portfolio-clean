from __future__ import annotations
from dataclasses import dataclass
import httpx

@dataclass
class ModelResponse:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
    provider: str = "mock"

class Provider:
    name="base"
    async def chat(self, messages, model: str) -> ModelResponse:
        raise NotImplementedError

class MockProvider(Provider):
    name="mock"
    async def chat(self, messages, model: str) -> ModelResponse:
        last=next((m["content"] for m in reversed(messages) if m["role"]=="user"), "")
        return ModelResponse(f"[JARVIS:{model}] {last}", max(1,len(last)//4), 1)

class OpenAICompatibleProvider(Provider):
    name="openai-compatible"
    def __init__(self, base_url: str, api_key: str):
        self.base_url=base_url.rstrip("/")
        self.api_key=api_key
    async def chat(self, messages, model: str) -> ModelResponse:
        headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"}
        async with httpx.AsyncClient(timeout=120) as client:
            r=await client.post(f"{self.base_url}/chat/completions",
                headers=headers,json={"model":model,"messages":messages})
            r.raise_for_status()
            data=r.json()
        choice=data["choices"][0]["message"]["content"]
        usage=data.get("usage",{})
        return ModelResponse(choice, usage.get("prompt_tokens",0), usage.get("completion_tokens",0), self.name)

class ProviderRouter:
    def __init__(self, primary: Provider, auxiliary: Provider):
        self.primary=primary
        self.auxiliary=auxiliary
    async def route(self, role: str, messages, model: str) -> ModelResponse:
        return await (self.auxiliary if role=="auxiliary" else self.primary).chat(messages, model)
