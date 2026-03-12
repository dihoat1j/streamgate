import yaml
from typing import List
from .providers.openai import OpenAIProvider
from .providers.base import BaseProvider

class GatewayConfig:
    def __init__(self, providers: List[BaseProvider]):
        self.providers = providers

    @classmethod
    def load(cls, path: str) -> "GatewayConfig":
        # In a real app, this would parse the YAML file
        # Mocking for demonstration
        providers = [
            OpenAIProvider("gpt-4-primary", "sk-...", "https://api.openai.com/v1"),
            OpenAIProvider("gpt-4-backup", "sk-...", "https://api.openai.com/v1")
        ]
        return cls(providers)
