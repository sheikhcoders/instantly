"""
OpenAI-compatible client for Hugging Face Inference Providers
"""

import os
from typing import List, Dict, Any, Optional
import openai
from .exceptions import ConfigurationError, APIError

class OpenAIClient:
    """
    OpenAI-compatible client for accessing Hugging Face Inference Providers
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://router.huggingface.co/v1",
    ):
        """
        Initialize the OpenAI-compatible client

        Args:
            api_key: Hugging Face API token. If not provided, will look for HF_TOKEN env variable
            base_url: Base URL for the Hugging Face Inference API
        """
        self.api_key = api_key or os.environ.get("HF_TOKEN")
        if not self.api_key:
            raise ConfigurationError("API key must be provided or set as HF_TOKEN environment variable")
        
        self.client = openai.Client(
            api_key=self.api_key,
            base_url=base_url,
        )

    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Create a chat completion using the specified model

        Args:
            model: The model to use (e.g., "moonshotai/Kimi-K2-Instruct")
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional arguments to pass to the completion API

        Returns:
            The completion response from the model
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            return response
        except Exception as e:
            raise APIError(f"Chat completion failed: {str(e)}")

    def embeddings(
        self,
        model: str,
        input: str | List[str],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Get embeddings for the provided text."""
        try:
            response = self.client.embeddings.create(
                model=model,
                input=input,
                **kwargs
            )
            return response
        except Exception as e:
            raise APIError(f"Embedding generation failed: {str(e)}")