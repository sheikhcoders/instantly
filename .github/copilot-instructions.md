# AI Agent Instructions for Instantly

## Project Overview
Instantly is a Python library that provides a unified interface for Hugging Face Inference Providers with OpenAI API compatibility. It enables seamless integration with 15+ inference partners under a single endpoint.

## Built-in Tools and Models

### Supported Tools
1. `DuckDuckGoSearchTool`
   - Web search using DuckDuckGo engine
   - Example:
   ```python
   from instantly import DuckDuckGoSearchTool
   search_tool = DuckDuckGoSearchTool(max_results=5)
   results = search_tool("Hugging Face")
   ```

2. `WebSearchTool`
   - Configurable web search with different engines
   - Example:
   ```python
   from instantly import WebSearchTool
   web_tool = WebSearchTool(max_results=10, engine="duckduckgo")
   ```

3. `VisitWebpageTool`
   - Fetch and process webpage content
   - Handles output length limits automatically

### Integration with Agent Systems
- All tools follow standard interface patterns
- Each tool validates inputs and handles errors uniformly
- Tools can be composed into larger workflows
- Browser automation agent with lifecycle hooks and state tracking
- Example:
  ```python
  agent = Agent(task="Browse documentation",
               llm=OpenAIClient())
  
  async def step_hook(agent):
      print(f"Current URL: {await agent.browser_session.get_current_page_url()}")
  
  await agent.run(on_step_start=step_hook)
  ```

## Architecture and Components

### Key Components
1. `OpenAIClient` (`instantly/openai_client.py`)
   - OpenAI-compatible interface for HF Inference Providers
   - Uses OpenAI's API patterns with HF backend
   - Example usage:
   ```python
   client = OpenAIClient(api_key="hf_token")
   response = client.chat_completion(
       model="moonshotai/Kimi-K2-Instruct",
       messages=[{"role": "user", "content": "Hello"}]
   )
   ```

2. `InferenceClient` (`instantly/client.py`)
   - Direct interface to HF Inference API
   - Specialized for image generation tasks
   - Example usage:
   ```python
   client = InferenceClient(api_key="hf_token")
   image = client.text_to_image(
       prompt="A landscape",
       model="black-forest-labs/FLUX.1-dev"
   )
   ```

## Development Workflow

### Environment Setup
1. Python 3.8+ required
2. Required environment variables:
   - `HF_TOKEN`: Hugging Face API token (Pro account required for some models)
   - Create token with appropriate scopes at https://huggingface.co/settings/tokens

### Configuration Management
1. Environment-specific settings in `.env` files:
   ```
   HF_TOKEN=<your huggingface token>
   OPENAI_BASE_URL=https://router.huggingface.co/v1
   ```
2. Never commit sensitive credentials - use environment variables

### Dependencies
Key dependencies (from `setup.py`):
- `openai>=1.0.0`: For OpenAI-compatible interface
- `huggingface_hub>=0.19.0`: For HF API access
- `pillow>=10.0.0`: For image handling
- `requests>=2.31.0`: For HTTP requests

### Testing
- Uses pytest framework with pytest-asyncio for async tests
- Mock clients available for testing: `from instantly.testing import MockLLMClient`
- Tests automatically skip if required credentials missing
- Run tests with: `python -m pytest tests/`
- Example test:
  ```python
  @pytest.mark.asyncio
  async def test_agent():
      agent = Agent(task="Test task", is_test=True)  # Uses mock client
      await agent.run(max_steps=1)
  ```

## Project Conventions

### Error Handling
- Custom exceptions in `instantly/exceptions.py`
- Configuration errors inherit from `InstantlyError`
- Always validate API tokens before client initialization

### API Design
1. All clients support both explicit API key and environment variable
2. Methods follow OpenAI naming conventions where applicable
3. All API methods support additional kwargs for flexibility

## Integration Points

### External Services
1. Hugging Face Inference API
   - Base URL: `https://router.huggingface.co/v1`
   - Requires HF API token for authentication

### Provider Support
- Multiple providers supported through Hugging Face (e.g., Together AI, Fireworks)
- Provider-specific options passed through kwargs

### Deployment
1. Local Development:
   ```python
   import os
   from instantly import OpenAIClient
   
   client = OpenAIClient(
       base_url="https://router.huggingface.co/v1",
       api_key=os.environ["HF_TOKEN"]
   )
   ```

2. Production Setup:
   - Use environment variables for all credentials
   - Implement proper error handling and retries
   - Monitor rate limits for each provider
   - Consider caching for frequent operations

### Streaming Patterns
All clients support streaming responses with OpenAI-compatible interfaces:
```python
stream = client.stream_chat_completion(
    model="model_name",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
)
for chunk in stream:
    content = chunk["choices"][0]["delta"]["content"]
    # Process chunk...
```

### Event-Driven Architecture
The browser automation agent uses an event bus system:
```python
# Event listener registration
async def on_url_change(event):
    print(f"URL changed to: {event.url}")
session.event_bus.listeners["URLChangeEvent"] = [on_url_change]

# State tracking
agent.state.record_thought("Planning next action...")
agent.state.record_action({"type": "navigate", "url": url})
```