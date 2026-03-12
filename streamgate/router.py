import random
from typing import List, Optional
from .providers.base import BaseProvider

class LoadBalancer:
    def __init__(self, providers: List[BaseProvider]):
        self.providers = providers
        self.index = 0

    def get_next_provider(self) -> Optional[BaseProvider]:
        active = [p for p in self.providers if p.is_healthy]
        if not active:
            return None
        
        # Simple Round Robin
        provider = active[self.index % len(active)]
        self.index += 1
        return provider

    def get_fallback(self, failed_provider: BaseProvider) -> Optional[BaseProvider]:
        for p in self.providers:
            if p != failed_provider and p.is_healthy:
                return p
        return None

    def get_status(self) -> List[dict]:
        return [
            {"name": p.name, "healthy": p.is_healthy, "latency": p.last_latency}
            for p in self.providers
        ]
