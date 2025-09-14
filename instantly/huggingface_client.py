import os
import json
import requests
from typing import Any, Dict, Generator, Optional

from .exceptions import ConfigurationError


class HuggingFaceClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api-inference.huggingface.co/v1"):
        self.base_url = base_url
        self.api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ConfigurationError(
                "API key must be provided or set as HUGGINGFACE_API_KEY environment variable"
            )

    def chat_completion(self, model: str, messages: list, **kwargs) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": model, "messages": messages, **kwargs},
        )
        response.raise_for_status()
        return response.json()

    def stream_chat_completion(self, model: str, messages: list, **kwargs) -> Generator[Dict[str, Any], None, None]:
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": model, "messages": messages, "stream": True, **kwargs},
            stream=True,
        )
        response.raise_for_status()
        for line in response.iter_lines():
            if line.startswith(b"data:"):
                if line.strip() == b"data: [DONE]":
                    return
                yield json.loads(line.decode("utf-8").lstrip("data:").rstrip("/n"))
