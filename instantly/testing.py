"""Mock client for testing."""
from typing import Dict, Any, List, Optional

class MockLLMClient:
    """Mock LLM client for testing."""
    
    def __init__(self, responses: Optional[List[Dict[str, Any]]] = None):
        """Initialize mock client.
        
        Args:
            responses: Optional list of predefined responses to return
        """
        self.responses = responses or []
        self.calls = []

    def chat_completion(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Mock chat completion."""
        self.calls.append({"model": model, "messages": messages, "kwargs": kwargs})
        if self.responses:
            return self.responses.pop(0)
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "Mock response"
                }
            }]
        }

    def stream_chat_completion(self, model: str, messages: List[Dict[str, str]], **kwargs):
        """Mock streaming chat completion."""
        self.calls.append({"model": model, "messages": messages, "kwargs": kwargs})
        yield {
            "choices": [{
                "delta": {
                    "role": "assistant",
                    "content": "Mock"
                }
            }]
        }
        yield {
            "choices": [{
                "delta": {
                    "role": "assistant",
                    "content": " response"
                }
            }]
        }