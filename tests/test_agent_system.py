"""Tests for the general-purpose AI Agent system."""

import pytest
import asyncio
import os
from typing import Dict, Any

from instantly.agent import Agent
from instantly.tools import (
    BaseTool,
    ToolMetadata,
    DuckDuckGoSearchTool,
    WebSearchTool,
    VisitWebpageTool,
    FileSystemTool,
    SQLiteDatabaseTool,
    APIRequestTool
)
from instantly.sandbox import Sandbox, ResourceLimits
from instantly.state import AgentState, EventBus
from instantly.exceptions import ValidationError

# Test tool for validation
class EchoTool(BaseTool):
    """Simple echo tool for testing."""
    
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="echo",
            description="Echo the input",
            tags=["test"]
        )
    
    def __call__(self, message: str) -> str:
        return message

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization with tools."""
    tools = [EchoTool()]
    agent = Agent(
        task="Test task",
        tools=tools,
        is_test=True
    )
    
    assert len(agent.tools) == 1
    assert "echo" in agent.tools

@pytest.mark.asyncio
async def test_tool_execution():
    """Test tool execution in sandbox."""
    agent = Agent(
        task="Test task",
        tools=[EchoTool()],
        is_test=True
    )
    
    result = await agent.execute_tool("echo", "Hello World")
    assert result == "Hello World"

@pytest.mark.asyncio
async def test_file_system_tool():
    """Test file system operations."""
    test_file = "test.txt"
    tool = FileSystemTool()
    
    # Write
    tool("write", test_file, "Hello World")
    assert os.path.exists(test_file)
    
    # Read
    content = tool("read", test_file)
    assert content == "Hello World"
    
    # Delete
    tool("delete", test_file)
    assert not os.path.exists(test_file)

@pytest.mark.asyncio
async def test_sqlite_tool():
    """Test SQLite operations."""
    db_file = "test.db"
    tool = SQLiteDatabaseTool(db_file)
    
    # Create table
    tool("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    
    # Insert
    tool("INSERT INTO test (value) VALUES (?)", ("test value",))
    
    # Select
    results = tool("SELECT value FROM test")
    assert results == [("test value",)]
    
    # Cleanup
    os.remove(db_file)

@pytest.mark.asyncio
async def test_api_request_tool():
    """Test API request tool."""
    tool = APIRequestTool(base_url="https://httpbin.org")
    
    # GET request
    result = tool("get", "get", params={"key": "value"})
    assert result["args"]["key"] == "value"
    
    # POST request
    data = {"test": "data"}
    result = tool("post", "post", data=data)
    assert result["json"]["test"] == "data"

@pytest.mark.asyncio
async def test_event_system():
    """Test event system."""
    agent = Agent(
        task="Test task",
        tools=[EchoTool()],
        is_test=True
    )
    
    events = []
    async def event_listener(event):
        events.append(event)
    
    agent.event_bus.subscribe("ToolExecutionEvent", event_listener)
    await agent.execute_tool("echo", "Hello")
    
    assert len(events) == 1
    assert events[0].tool_name == "echo"
    assert events[0].result == "Hello"

@pytest.mark.asyncio
async def test_resource_limits():
    """Test resource limits in sandbox."""
    agent = Agent(
        task="Test task",
        tools=[EchoTool()],
        sandbox_config={
            "resource_limits": ResourceLimits(
                max_memory=1024 * 1024,  # 1MB
                max_cpu_time=1,
                max_file_size=1024
            )
        },
        is_test=True
    )
    
    # Should execute within limits
    result = await agent.execute_tool("echo", "Hello")
    assert result == "Hello"

@pytest.mark.asyncio
async def test_state_management():
    """Test state management."""
    agent = Agent(
        task="Test task",
        tools=[EchoTool()],
        is_test=True
    )
    
    # Set state
    await agent.state.set("test_key", "test_value")
    assert agent.state.get("test_key") == "test_value"
    
    # Update state
    await agent.state.set("test_key", "new_value")
    assert agent.state.get("test_key") == "new_value"
    
    # Delete state
    agent.state.delete("test_key")
    assert agent.state.get("test_key") is None