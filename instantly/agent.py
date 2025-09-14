"""
General-purpose AI Agent with tool support and sandbox execution.
"""

import asyncio
from typing import Any, Callable, Dict, List, Optional
from pathlib import Path

from .openai_client import OpenAIClient
from .google_client import GoogleAIClient
from .exceptions import ConfigurationError
from .tools import ToolRegistry, BaseTool
from .sandbox import Sandbox, ResourceLimits
from .state import AgentState, EventBus, ToolExecutionEvent

class BrowserSession:
    """Manages browser interaction and state."""
    
    def __init__(self):
        self.current_url: Optional[str] = None
        self.tabs: List[Dict[str, str]] = []
        self.event_bus = EventBus()
        self.agent_focus = None

    async def get_browser_state_summary(self) -> Dict[str, Any]:
        """Get current browser state summary."""
        return {
            "url": self.current_url,
            "tabs": self.tabs,
            "focus": self.agent_focus
        }

    async def get_or_create_cdp_session(self):
        """Get or create a new CDP session."""
        if not self.agent_focus:
            # Initialize new session
            pass
        return self.agent_focus

    async def get_current_page_url(self) -> Optional[str]:
        """Get URL of current active tab."""
        return self.current_url

    async def get_current_page_title(self) -> Optional[str]:
        """Get title of current active tab."""
        if not self.tabs:
            return None
        return next((tab.get("title") for tab in self.tabs if tab.get("active")), None)

    async def get_tabs(self) -> List[Dict[str, str]]:
        """Get all open tabs."""
        return self.tabs.copy()

class EventBus:
    """Simple event system for browser interactions."""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def dispatch(self, event: Any):
        """Dispatch an event to registered listeners."""
        event_type = type(event).__name__
        listeners = self.listeners.get(event_type, [])
        for listener in listeners:
            asyncio.create_task(listener(event))
        return event

class AgentState:
    """Tracks agent execution state and history."""
    
    def __init__(self):
        self.thoughts: List[str] = []
        self.outputs: List[str] = []
        self.actions: List[Dict[str, Any]] = []
        self.visited_urls: List[str] = []
        self.extracted_content: List[Dict[str, Any]] = []

    def record_thought(self, thought: str):
        """Record agent reasoning."""
        self.thoughts.append(thought)

    def record_output(self, output: str):
        """Record model output."""
        self.outputs.append(output)

    def record_action(self, action: Dict[str, Any]):
        """Record agent action."""
        self.actions.append(action)

    def record_url(self, url: str):
        """Record visited URL."""
        self.visited_urls.append(url)

    def record_content(self, content: Dict[str, Any]):
        """Record extracted content."""
        self.extracted_content.append(content)

class Agent:
    """
    General-purpose AI Agent with tool support and sandbox execution.
    """
    
    def __init__(
        self,
        task: str,
        llm: Optional[Any] = None,
        tools: Optional[List[BaseTool]] = None,
        context: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
        sensitive_data: Optional[Dict[str, Any]] = None,
        sandbox_config: Optional[Dict[str, Any]] = None,
        is_test: bool = False,
    ):
        """
        Initialize general-purpose AI agent.

        Args:
            task: Main task description
            llm: Language model client (OpenAI, Google, or Mock)
            tools: List of tools to register
            context: Additional context data
            settings: Configuration settings
            sensitive_data: Sensitive data to protect
            sandbox_config: Sandbox configuration
            is_test: Whether this is a test instance
        """
        self.task = task
        from .testing import MockLLMClient
        self.llm = llm or (MockLLMClient() if is_test else OpenAIClient())
        self.context = context or {}
        self.settings = settings or {}
        self.sensitive_data = sensitive_data or {}
        self.sandbox_config = sandbox_config or {}
        
        # Initialize components
        self.event_bus = EventBus()
        self.state = AgentState(event_bus=self.event_bus)
        self.tool_registry = ToolRegistry()
        self.browser_session = BrowserSession()
        
        # Register tools
        if tools:
            for tool in tools:
                self.tool_registry.register(tool)
        
        self._paused = False
        self._on_step_start = None
        self._on_step_end = None
        self._max_steps = None

    def pause(self):
        """Pause agent execution."""
        self._paused = True

    def resume(self):
        """Resume agent execution."""
        self._paused = False

    def add_new_task(self, task: str):
        """Queue a new task for execution."""
        # Implementation for task queueing
        pass

    async def run(
        self,
        on_step_start: Optional[Callable[["Agent"], Any]] = None,
        on_step_end: Optional[Callable[["Agent"], Any]] = None,
        max_steps: Optional[int] = None,
    ):
        """
        Run the agent with lifecycle hooks.

        Args:
            on_step_start: Hook called before each step
            on_step_end: Hook called after each step
            max_steps: Maximum number of steps to execute
        """
        self._on_step_start = on_step_start
        self._on_step_end = on_step_end
        self._max_steps = max_steps

        step = 0
        while not self._paused and (max_steps is None or step < max_steps):
            # Execute step start hook
            if self._on_step_start:
                await self._on_step_start(self)

            # Process current state and decide next action
            await self._process_step()

            # Execute step end hook
            if self._on_step_end:
                await self._on_step_end(self)

            step += 1

    async def _process_step(self):
        """Process a single agent step."""
        # Implementation for state processing and action execution
        pass

    async def execute_tool(self, name: str, *args, **kwargs) -> Any:
        """Execute a tool in the sandbox."""
        try:
            result = await self.tool_registry.execute(
                name,
                *args,
                sandbox_config=self.sandbox_config,
                **kwargs
            )
            
            await self.event_bus.dispatch(ToolExecutionEvent(
                tool_name=name,
                args=args,
                kwargs=kwargs,
                result=result
            ))
            
            return result
        except Exception as e:
            await self.event_bus.dispatch(ToolExecutionEvent(
                tool_name=name,
                args=args,
                kwargs=kwargs,
                error=e
            ))
            raise
    
    @property
    def tools(self):
        """Access available tools and actions."""
        return {tool.name: tool for tool in self.tool_registry.list_tools()}

    @property
    def history(self):
        """Access historical execution data."""
        return {
            "model_thoughts": lambda: self.state.thoughts,
            "model_outputs": lambda: self.state.outputs,
            "model_actions": lambda: self.state.actions,
            "extracted_content": lambda: self.state.extracted_content,
            "urls": lambda: self.state.visited_urls,
        }