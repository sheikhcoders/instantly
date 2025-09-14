import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from .exceptions import ConfigurationError, APIError

class GoogleAIClient:
    """
    GoogleAIClient for interacting with Google's Generative AI models (Gemini).
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the GoogleAIClient.

        Args:
            api_key (Optional[str]): The API key for Google's Generative AI.
                                     If not provided, it will be read from the
                                     GOOGLE_API_KEY environment variable.

        Raises:
            ConfigurationError: If the API key is not provided and cannot be
                                found in the environment variables.
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ConfigurationError(
                "API key must be provided or set as GOOGLE_API_KEY environment variable"
            )
        genai.configure(api_key=self.api_key)
        self.client = genai

    def chat_completion(
        self, model: str, messages: List[Dict[str, str]], **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Generates a chat completion response from the specified model.

        Args:
            model (str): The name of the model to use for the chat completion.
            messages (List[Dict[str, str]]): A list of message dictionaries,
                                             where each dictionary has a "role"
                                             and "content".
            **kwargs: Additional keyword arguments to be passed to the model.

        Returns:
            Dict[str, Any]: A dictionary representing the chat completion
                            response, formatted to be compatible with OpenAI's
                            API structure.
        
        Raises:
            APIError: If the chat completion request fails.
        """
        try:
            generation_config = self.client.types.GenerationConfig(**kwargs)
            response = self.client.GenerativeModel(model).generate_content(
                contents=[
                    {"role": msg["role"], "parts": [msg["content"]]} for msg in messages
                ],
                generation_config=generation_config,
            )
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": response.text,
                        }
                    }
                ]
            }
        except Exception as e:
            raise APIError(f"Chat completion failed: {e}")

    def stream_chat_completion(
        self, model: str, messages: List[Dict[str, str]], **kwargs: Any
    ):
        """
        Streams a chat completion response from the specified model.

        Args:
            model (str): The name of the model to use for the chat completion.
            messages (List[Dict[str, str]]): A list of message dictionaries.
            **kwargs: Additional keyword arguments to be passed to the model.

        Yields:
            Dict[str, Any]: A dictionary for each chunk of the streamed
                            response, formatted to be compatible with OpenAI's
                            API structure.
        
        Raises:
            APIError: If the streaming chat completion request fails.
        """
        try:
            generation_config = self.client.types.GenerationConfig(**kwargs)
            response = self.client.GenerativeModel(model).generate_content(
                contents=[
                    {"role": msg["role"], "parts": [msg["content"]]} for msg in messages
                ],
                generation_config=generation_config,
                stream=True,
            )
            for chunk in response:
                yield {
                    "choices": [
                        {
                            "delta": {
                                "role": "assistant",
                                "content": chunk.text,
                            }
                        }
                    ]
                }
        except Exception as e:
            raise APIError(f"Streaming chat completion failed: {e}")
