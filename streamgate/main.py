import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from .router import LoadBalancer
from .config import GatewayConfig
from .providers.base import BaseProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stream-gate")

class StreamGate:
    def __init__(self, config_path: str):
        self.config = GatewayConfig.load(config_path)
        self.balancer = LoadBalancer(self.config.providers)
        self.app = FastAPI(title="StreamGate LLM Proxy")
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/v1/chat/completions")
        async def chat_completions(request: Request):
            body = await request.json()
            stream = body.get("stream", False)
            
            provider = self.balancer.get_next_provider()
            if not provider:
                raise HTTPException(status_code=503, detail="No providers available")

            try:
                if stream:
                    return StreamingResponse(
                        provider.stream_chat(body),
                        media_type="text/event-stream"
                    )
                return await provider.chat(body)
            except Exception as e:
                logger.error(f"Provider {provider.name} failed: {str(e)}")
                # Fallback logic
                fallback = self.balancer.get_fallback(provider)
                if fallback:
                    return await fallback.chat(body)
                raise HTTPException(status_code=500, detail="All providers failed")

        @self.app.get("/health")
        async def health():
            return {"status": "ok", "providers": self.balancer.get_status()}

def create_app():
    gate = StreamGate("config.yaml")
    return gate.app
