import abc
import time
from typing import AsyncIterable, Dict, Any

class BaseProvider(abc.ABC):
    def __init__(self, name: str, api_key: str, base_url: str):
        self.name = name
        self.api_key = api_key
        self.base_url = base_url
        self.is_healthy = True
        self.last_latency = 0.0

    @abc.abstractmethod
    async def chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    async def stream_chat(self, payload: Dict[str, Any]) -> AsyncIterable[str]:
        pass

    def mark_failed(self):
        self.is_healthy = False
        
    def mark_healthy(self, latency: float):
        self.is_healthy = True
        self.last_latency = latency
