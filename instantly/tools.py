import inspect
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type, Callable
from dataclasses import dataclass
from .exceptions import ValidationError, APIError
from .sandbox import Sandbox, ResourceLimits

@dataclass
class ToolMetadata:
    """Metadata for a tool."""
    name: str
    description: str
    version: str = "1.0.0"
    author: str = ""
    tags: List[str] = None
    requires_auth: bool = False
    is_async: bool = False

class BaseTool(ABC):
    """Base class for all tools."""
    
    def __init__(self):
        self.metadata = self._get_metadata()
        self._validate_implementation()
    
    @abstractmethod
    def _get_metadata(self) -> ToolMetadata:
        """Get tool metadata."""
        pass
    
    def _validate_implementation(self):
        """Validate tool implementation."""
        if not hasattr(self, '__call__'):
            raise ValidationError(f"Tool {self.__class__.__name__} must implement __call__ method")
    
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        """Execute the tool."""
        pass

class ToolRegistry:
    """Registry for managing and executing tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        """Register a new tool."""
        metadata = tool._get_metadata()
        if metadata.name in self._tools:
            raise ValidationError(f"Tool {metadata.name} is already registered")
        self._tools[metadata.name] = tool
    
    def unregister(self, name: str):
        """Unregister a tool."""
        if name not in self._tools:
            raise ValidationError(f"Tool {name} is not registered")
        del self._tools[name]
    
    def get_tool(self, name: str) -> BaseTool:
        """Get a registered tool."""
        if name not in self._tools:
            raise ValidationError(f"Tool {name} is not registered")
        return self._tools[name]
    
    def list_tools(self) -> List[ToolMetadata]:
        """List all registered tools."""
        return [tool._get_metadata() for tool in self._tools.values()]
    
    async def execute(
        self,
        name: str,
        *args,
        sandbox_config: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """Execute a tool in a sandbox."""
        tool = self.get_tool(name)
        sandbox_config = sandbox_config or {}
        
        return await Sandbox.run(
            tool,
            *args,
            **{**sandbox_config, **kwargs}
        )

class DuckDuckGoSearchTool(BaseTool):
    """Web search using DuckDuckGo engine."""
    
    def __init__(self, max_results: int = 5):
        super().__init__()
        self.max_results = max_results
        self.base_url = "https://api.duckduckgo.com"
    
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="duckduckgo_search",
            description="Web search using DuckDuckGo engine",
            tags=["search", "web"],
            requires_auth=False,
            is_async=False
        )
    
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

class WebSearchTool(BaseTool):
    """Configurable web search with different engines."""
    
    def __init__(
        self,
        max_results: int = 10,
        engine: str = "duckduckgo"
    ):
        super().__init__()
        if engine not in ["duckduckgo"]:
            raise ValidationError(f"Unsupported search engine: {engine}")
        
        self.engine = engine
        self.max_results = max_results
        self._search_tool = DuckDuckGoSearchTool(max_results=max_results)
    
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="web_search",
            description="Configurable web search with different engines",
            tags=["search", "web"],
            requires_auth=False,
            is_async=False
        )
    
    def __call__(self, query: str) -> List[Dict[str, str]]:
        """Execute a search query using the configured engine."""
        return self._search_tool(query)

class VisitWebpageTool(BaseTool):
    """Fetch and process webpage content."""
    
    def __init__(self, max_length: Optional[int] = None):
        super().__init__()
        self.max_length = max_length
    
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="visit_webpage",
            description="Fetch and process webpage content",
            tags=["web", "content"],
            requires_auth=False,
            is_async=False
        )

class FileSystemTool(BaseTool):
    """File system operations tool."""
    
    def __init__(self, base_path: str = "."):
        super().__init__()
        self.base_path = base_path
    
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="filesystem",
            description="File system operations",
            tags=["file", "system", "io"],
            requires_auth=False,
            is_async=False
        )
    
    def __call__(self, operation: str, path: str, content: Optional[str] = None) -> Any:
        """Execute a file system operation."""
        full_path = os.path.join(self.base_path, path)
        
        if operation == "read":
            with open(full_path, 'r') as f:
                return f.read()
        elif operation == "write":
            if content is None:
                raise ValidationError("Content required for write operation")
            with open(full_path, 'w') as f:
                f.write(content)
        elif operation == "delete":
            os.remove(full_path)
        elif operation == "exists":
            return os.path.exists(full_path)
        else:
            raise ValidationError(f"Unsupported operation: {operation}")

class SQLiteDatabaseTool(BaseTool):
    """SQLite database operations tool."""
    
    def __init__(self, db_path: str):
        super().__init__()
        self.db_path = db_path
        
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="sqlite",
            description="SQLite database operations",
            tags=["database", "sql"],
            requires_auth=False,
            is_async=False
        )
    
    def __call__(self, query: str, params: Optional[tuple] = None) -> Any:
        """Execute a SQL query."""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

class APIRequestTool(BaseTool):
    """API request tool."""
    
    def __init__(self, base_url: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        super().__init__()
        self.base_url = base_url
        self.headers = headers or {}
    
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="api_request",
            description="Make HTTP API requests",
            tags=["api", "http", "web"],
            requires_auth=False,
            is_async=False
        )
    
    def __call__(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None
    ) -> Any:
        """Make an HTTP request."""
        url = f"{self.base_url}/{endpoint}" if self.base_url else endpoint
        
        response = requests.request(
            method=method.upper(),
            url=url,
            json=data,
            params=params,
            headers=self.headers
        )
        response.raise_for_status()
        
        return response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
    
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