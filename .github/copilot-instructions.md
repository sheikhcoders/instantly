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
- Uses pytest framework
- Current focus on configuration validation
- Run tests with: `python -m pytest tests/`

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