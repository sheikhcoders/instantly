"""
Generator module for text and image generation using Google's Gemini model.
"""

import base64
import mimetypes
import os
from typing import Dict, Any, List, Optional, Union
import google.generativeai as genai
from google.generativeai import types
from .exceptions import ConfigurationError, APIError

class Generator:
    """Content generator using Google's Gemini model."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the generator.

        Args:
            api_key: Gemini API key. If not provided, will look for GEMINI_API_KEY in environment.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ConfigurationError("API key must be provided either explicitly or via GEMINI_API_KEY environment variable")
        
        genai.configure(api_key=self.api_key)
        self.client = genai

    def generate(
        self,
        prompt: str,
        model: str = "gemini-2.5-flash-image-preview",
        response_modalities: List[str] = ["IMAGE", "TEXT"],
        system_instruction: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate content using specified model.
        
        Args:
            prompt: Text prompt for generation
            model: Model name to use
            response_modalities: List of desired output modalities
            system_instruction: Optional system instruction
            **kwargs: Additional parameters for generation
            
        Returns:
            Generated content response
        """
        try:
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            ]

            config = types.GenerateContentConfig(
                response_modalities=response_modalities,
                system_instruction=[
                    types.Part.from_text(text=system_instruction)
                ] if system_instruction else None,
                **kwargs
            )

            response = self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=config
            )
            
            return self._process_response(response)
        except Exception as e:
            raise APIError(f"Content generation failed: {str(e)}")

    def save_binary_file(
        self,
        file_name: str,
        data: Union[str, bytes],
        file_extension: Optional[str] = None
    ) -> str:
        """Save binary data to a file.
        
        Args:
            file_name: Name for the output file
            data: Binary data to save
            file_extension: Optional file extension override
            
        Returns:
            Path to saved file
        """
        try:
            # Convert string data to bytes if needed
            if isinstance(data, str):
                data = base64.b64decode(data)
                
            # Add extension if provided
            if file_extension:
                file_name = f"{file_name}{file_extension}"
                
            with open(file_name, "wb") as f:
                f.write(data)
                
            return file_name
        except Exception as e:
            raise APIError(f"Failed to save file: {str(e)}")

    def _process_response(self, response: Any) -> Dict[str, Any]:
        """Process streaming response into structured output.
        
        Args:
            response: Raw streaming response
            
        Returns:
            Processed response data
        """
        output = {
            "text": "",
            "images": []
        }
        
        file_index = 0
        for chunk in response:
            if (chunk.candidates is None or 
                chunk.candidates[0].content is None or 
                chunk.candidates[0].content.parts is None):
                continue
                
            part = chunk.candidates[0].content.parts[0]
            
            if hasattr(part, "text") and part.text:
                output["text"] += part.text
                
            if hasattr(part, "inline_data") and part.inline_data:
                file_name = f"generated_image_{file_index}"
                file_extension = mimetypes.guess_extension(part.inline_data.mime_type)
                saved_path = self.save_binary_file(
                    file_name,
                    part.inline_data.data,
                    file_extension
                )
                output["images"].append(saved_path)
                file_index += 1
                
        return output
