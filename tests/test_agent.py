"""Tests for the browser automation agent."""

import asyncio
import pytest
from instantly.agent import Agent, BrowserSession, AgentState
from instantly.testing import MockLLMClient

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization with default settings."""
    task = "Test task"
    mock_llm = MockLLMClient()
    agent = Agent(task=task, llm=mock_llm)
    
    assert agent.task == task
    assert isinstance(agent.llm, MockLLMClient)
    assert isinstance(agent.browser_session, BrowserSession)
    assert isinstance(agent.state, AgentState)
    assert agent.context == {}
    assert agent.settings == {}
    assert agent.sensitive_data == {}

@pytest.mark.asyncio
async def test_agent_hooks():
    """Test agent lifecycle hooks."""
    start_called = False
    end_called = False

    async def on_start(agent):
        nonlocal start_called
        start_called = True

    async def on_end(agent):
        nonlocal end_called
        end_called = True

    agent = Agent(task="Test hooks", llm=MockLLMClient())
    await agent.run(
        on_step_start=on_start,
        on_step_end=on_end,
        max_steps=1
    )

    assert start_called
    assert end_called

@pytest.mark.asyncio
async def test_agent_state_recording():
    """Test agent state recording."""
    agent = Agent(task="Test state", is_test=True)
    
    # Record various state items
    agent.state.record_thought("Test thought")
    agent.state.record_output("Test output")
    agent.state.record_action({"type": "test"})
    agent.state.record_url("https://example.com")
    agent.state.record_content({"data": "test"})

    # Verify history access
    assert agent.history["model_thoughts"]() == ["Test thought"]
    assert agent.history["model_outputs"]() == ["Test output"]
    assert agent.history["model_actions"]() == [{"type": "test"}]
    assert agent.history["urls"]() == ["https://example.com"]
    assert agent.history["extracted_content"]() == [{"data": "test"}]

@pytest.mark.asyncio
async def test_browser_session():
    """Test browser session functionality."""
    session = BrowserSession()
    
    # Test initial state
    assert await session.get_current_page_url() is None
    assert await session.get_current_page_title() is None
    assert await session.get_tabs() == []

    # Test state updates
    session.current_url = "https://example.com"
    session.tabs = [{"url": "https://example.com", "title": "Example", "active": True}]

    state = await session.get_browser_state_summary()
    assert state["url"] == "https://example.com"
    assert len(state["tabs"]) == 1
    assert await session.get_current_page_title() == "Example"

@pytest.mark.asyncio
async def test_agent_pause_resume():
    """Test agent pause/resume functionality."""
    agent = Agent(task="Test pause/resume", llm=MockLLMClient())
    
    assert not agent._paused
    agent.pause()
    assert agent._paused
    agent.resume()
    assert not agent._paused

@pytest.mark.asyncio
async def test_event_bus():
    """Test event bus dispatch system."""
    session = BrowserSession()
    
    class TestEvent:
        def __init__(self, data):
            self.data = data
    
    received_event = None
    async def event_listener(event):
        nonlocal received_event
        received_event = event
    
    # Register listener
    session.event_bus.listeners["TestEvent"] = [event_listener]
    
    # Dispatch event
    test_event = TestEvent("test data")
    session.event_bus.dispatch(test_event)
    
    # Allow event to process
    await asyncio.sleep(0)
    
    assert received_event is test_event
    assert received_event.data == "test data"