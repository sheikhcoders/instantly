"""
instantly - A unified interface for Hugging Face Inference Providers and Google AI
"""

from .client import InferenceClient
from .openai_client import OpenAIClient
from .google_client import GoogleAIClient
from .generator import Generator
from .tools import DuckDuckGoSearchTool, WebSearchTool, VisitWebpageTool
from .exceptions import InstantlyError

__version__ = "0.1.0"
__all__ = [
    "OpenAIClient",
    "InferenceClient",
    "GoogleAIClient",
    "Generator",
    "DuckDuckGoSearchTool",
    "WebSearchTool",
    "VisitWebpageTool",
    "InstantlyError",
]
