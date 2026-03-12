import httpx
import json
import time
from typing import AsyncIterable, Dict, Any
from .base import BaseProvider

class OpenAIProvider(BaseProvider):
    async def chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30.0
            )
            if response.status_code != 200:
                self.mark_failed()
                raise Exception(f"OpenAI Error: {response.text}")
            
            self.mark_healthy(time.time() - start)
            return response.json()

    async def stream_chat(self, payload: Dict[str, Any]) -> AsyncIterable[str]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        yield f"{line}\n\n"
