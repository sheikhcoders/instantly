import os
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from .exceptions import ConfigurationError, APIError

class GoogleAIClient:
    """Google AI (Gemini) client for accessing Google's language models"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Google AI client.
        
        Args:
            api_key: Google AI API key. If not provided, will look for GEMINI_API_KEY in environment.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ConfigurationError("API key must be provided either explicitly or via GEMINI_API_KEY environment variable")
        
        self.client = genai.Client(api_key=self.api_key)

    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None,
        thinking_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Create a chat completion using the specified Google AI model

        Args:
            model: The model to use (e.g., "gemini-2.5-pro")
            messages: List of message dictionaries with 'role' and 'content'
            system_instruction: Optional system instruction to guide model behavior
            thinking_config: Optional configuration for model thinking settings
            **kwargs: Additional arguments to pass to the completion API

        Returns:
            The completion response from the model formatted in OpenAI-compatible structure
        """
        try:
            # Convert messages to Google AI format
            contents = []
            if system_instruction:
                contents.append(
                    types.Content(
                        role="system",
                        parts=[types.Part.from_text(text=system_instruction)]
                    )
                )

            for msg in messages:
                contents.append(
                    types.Content(
                        role=msg["role"],
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            # Configure generation settings
            config = types.GenerateContentConfig()
            if thinking_config:
                config.thinking_config = types.ThinkingConfig(**thinking_config)

            # Generate response
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
                **kwargs
            )

            # Format response to be consistent with OpenAI format
            completion_response = {
                "model": model,
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response.text
                    }
                }],
                "usage": {}  # Google AI doesn't provide token usage info
            }

            return completion_response

        except Exception as e:
            raise APIError(f"Chat completion failed: {str(e)}")

    def stream_chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None,
        thinking_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ):
        """
        Stream a chat completion using the specified Google AI model

        Args:
            model: The model to use (e.g., "gemini-2.5-pro")
            messages: List of message dictionaries with 'role' and 'content'
            system_instruction: Optional system instruction to guide model behavior
            thinking_config: Optional configuration for model thinking settings
            **kwargs: Additional arguments to pass to the completion API

        Returns:
            A generator yielding completion chunks from the model in OpenAI-compatible format
        """
        try:
            # Convert messages to Google AI format
            contents = []
            if system_instruction:
                contents.append(
                    types.Content(
                        role="system",
                        parts=[types.Part.from_text(text=system_instruction)]
                    )
                )

            for msg in messages:
                contents.append(
                    types.Content(
                        role=msg["role"],
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            # Configure generation settings
            config = types.GenerateContentConfig()
            if thinking_config:
                config.thinking_config = types.ThinkingConfig(**thinking_config)

            # Generate streaming response
            response = self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=config,
                **kwargs
            )

            for chunk in response:
                # Format chunk to be consistent with OpenAI format
                completion_chunk = {
                    "choices": [{
                        "delta": {
                            "role": "assistant",
                            "content": chunk.text
                        }
                    }]
                }
                yield completion_chunk

        except Exception as e:
            raise APIError(f"Streaming chat completion failed: {str(e)}")
            
    def list_models(self) -> Dict[str, Any]:
        """List available models and their capabilities."""
        try:
            return {"models": self.client.list_models()}
        except Exception as e:
            raise APIError(f"Failed to list models: {str(e)}")