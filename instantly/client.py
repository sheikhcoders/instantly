"""
Hugging Face Inference Client for direct API access
"""

import os
from typing import Optional, Dict, Any
import requests
from PIL import Image
from io import BytesIO
from .exceptions import ConfigurationError, APIError

class InferenceClient:
    """
    Client for direct access to Hugging Face Inference API
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://router.huggingface.co/v1"
    ):
        """
        Initialize the Inference client

        Args:
            api_key: Hugging Face API token. If not provided, will look for HF_TOKEN env variable
            base_url: Optional base URL for the Hugging Face Inference API
        """
        self.api_key = api_key or os.environ.get("HF_TOKEN")
        if not self.api_key:
            raise ConfigurationError("API key must be provided or set as HF_TOKEN environment variable")

        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def text_to_image(
        self,
        prompt: str,
        model: str,
        **kwargs: Any
    ) -> Image.Image:
        """
        Generate an image from text using the specified model

        Args:
            prompt: The text prompt to generate an image from
            model: The model to use (e.g., "black-forest-labs/FLUX.1-dev")
            **kwargs: Additional arguments to pass to the image generation API

        Returns:
            A PIL.Image object
        """
        try:
            response = self.session.post(
                f"{self.base_url}/models/{model}",
                json={"inputs": prompt, **kwargs}
            )
            response.raise_for_status()

            # Return as PIL Image
            return Image.open(BytesIO(response.content))
        except Exception as e:
            raise APIError(f"Image generation failed: {str(e)}")

    def text_generation(
        self,
        prompt: str,
        model: str,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Generate text using the specified model

        Args:
            prompt: The text prompt to generate completions for
            model: The model to use (e.g., "gpt-2", "distilgpt2")
            **kwargs: Additional arguments to pass to the text generation API

        Returns:
            A dictionary containing the generated text and other metadata
        """
        try:
            response = self.session.post(
                f"{self.base_url}/models/{model}",
                json={"inputs": prompt, **kwargs}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise APIError(f"Text generation failed: {str(e)}")