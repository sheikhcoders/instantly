import requests
from typing import List, Dict, Any, Optional
from .exceptions import ValidationError, APIError

class DuckDuckGoSearchTool:
    """Web search using DuckDuckGo engine."""
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
        self.base_url = "https://api.duckduckgo.com"
    
    def __call__(self, query: str) -> List[Dict[str, str]]:
        """Execute a search query."""
        try:
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            return results['RelatedTopics'][:self.max_results]
        except Exception as e:
            raise APIError(f"DuckDuckGo search failed: {str(e)}")

class WebSearchTool:
    """Configurable web search with different engines."""
    
    def __init__(
        self,
        max_results: int = 10,
        engine: str = "duckduckgo"
    ):
        if engine not in ["duckduckgo"]:
            raise ValidationError(f"Unsupported search engine: {engine}")
        
        self.engine = engine
        self.max_results = max_results
        self._search_tool = DuckDuckGoSearchTool(max_results=max_results)
    
    def __call__(self, query: str) -> List[Dict[str, str]]:
        """Execute a search query using the configured engine."""
        return self._search_tool(query)

class VisitWebpageTool:
    """Fetch and process webpage content."""
    
    def __init__(self, max_length: Optional[int] = None):
        self.max_length = max_length
    
    def __call__(self, url: str) -> str:
        """Fetch and return the content of a webpage."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            content = response.text
            if self.max_length and len(content) > self.max_length:
                content = content[:self.max_length]
            
            return content
        except Exception as e:
            raise APIError(f"Failed to fetch webpage: {str(e)}")