"""
State management and event system for agent operations.
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import json

@dataclass
class Event:
    """Base class for all events."""
    timestamp: datetime = field(default_factory=datetime.now)
    event_type: str = field(init=False)
    
    def __post_init__(self):
        self.event_type = self.__class__.__name__

@dataclass
class ToolExecutionEvent(Event):
    """Event for tool execution."""
    tool_name: str
    args: tuple
    kwargs: Dict[str, Any]
    result: Optional[Any] = None
    error: Optional[Exception] = None

@dataclass
class StateChangeEvent(Event):
    """Event for state changes."""
    key: str
    old_value: Any
    new_value: Any

class EventBus:
    """Event system for agent operations."""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._history: List[Event] = []
    
    def subscribe(self, event_type: str, listener: Callable):
        """Subscribe to events of a specific type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
    
    def unsubscribe(self, event_type: str, listener: Callable):
        """Unsubscribe from events of a specific type."""
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)
    
    async def dispatch(self, event: Event):
        """Dispatch an event to registered listeners."""
        self._history.append(event)
        
        listeners = self._listeners.get(event.event_type, [])
        tasks = [listener(event) for listener in listeners]
        
        if tasks:
            await asyncio.gather(*tasks)
    
    def get_history(self, event_type: Optional[str] = None) -> List[Event]:
        """Get event history, optionally filtered by type."""
        if event_type:
            return [e for e in self._history if e.event_type == event_type]
        return list(self._history)

class AgentState:
    """State management for agent operations."""
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        self._state: Dict[str, Any] = {}
        self._event_bus = event_bus or EventBus()
    
    async def set(self, key: str, value: Any):
        """Set a state value."""
        old_value = self._state.get(key)
        self._state[key] = value
        
        await self._event_bus.dispatch(StateChangeEvent(
            key=key,
            old_value=old_value,
            new_value=value
        ))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self._state.get(key, default)
    
    def delete(self, key: str):
        """Delete a state value."""
        if key in self._state:
            del self._state[key]
    
    @property
    def event_bus(self) -> EventBus:
        """Get the event bus."""
        return self._event_bus
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return dict(self._state)
    
    def load_dict(self, data: Dict[str, Any]):
        """Load state from dictionary."""
        self._state = dict(data)