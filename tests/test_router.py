import pytest
from streamgate.router import LoadBalancer
from streamgate.providers.base import BaseProvider

class MockProvider(BaseProvider):
    async def chat(self, p): return {}
    async def stream_chat(self, p): yield ""

def test_load_balancer_round_robin():
    p1 = MockProvider("p1", "", "")
    p2 = MockProvider("p2", "", "")
    lb = LoadBalancer([p1, p2])
    
    assert lb.get_next_provider() == p1
    assert lb.get_next_provider() == p2
    assert lb.get_next_provider() == p1

def test_load_balancer_failover():
    p1 = MockProvider("p1", "", "")
    p2 = MockProvider("p2", "", "")
    p1.mark_failed()
    lb = LoadBalancer([p1, p2])
    
    assert lb.get_next_provider() == p2
