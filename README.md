# Instantly

A unified interface for Hugging Face Inference Providers and Google AI with OpenAI API compatibility.

## Installation

```bash
pip install instantly
```

## Configuration

Set your API keys in environment variables:

```bash
export HF_TOKEN=your_huggingface_token
export GEMINI_API_KEY=your_google_ai_token
```

Or use a .env file:

```
HF_TOKEN=your_huggingface_token
GEMINI_API_KEY=your_google_ai_token
OPENAI_BASE_URL=https://router.huggingface.co/v1
```

## Usage

### OpenAI-Compatible Interface

```python
from instantly import OpenAIClient

client = OpenAIClient(api_key="hf_token")
response = client.chat_completion(
    model="moonshotai/Kimi-K2-Instruct",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Hugging Face Direct Interface

```python
from instantly import InferenceClient

client = InferenceClient(api_key="hf_token")
image = client.text_to_image(
    prompt="A landscape",
    model="black-forest-labs/FLUX.1-dev"
)
```

### Google AI Interface

```python
from instantly import GoogleAIClient

client = GoogleAIClient(api_key="your_gemini_key")
response = client.generate_content(
    model="gemini-2.5-flash-image-preview",
    prompt="Hello, how are you?"
)
```

### Search Tools

```python
from instantly import DuckDuckGoSearchTool, WebSearchTool, VisitWebpageTool

# DuckDuckGo search
search = DuckDuckGoSearchTool(max_results=5)
results = search("Hugging Face")

# Web search with configurable engine
web_search = WebSearchTool(max_results=10, engine="duckduckgo")
results = web_search("Machine Learning")

# Visit and process webpage
webpage = VisitWebpageTool()
content = webpage("https://example.com")
```

## Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/instantly.git
cd instantly
```

2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

3. Run tests:

```bash
python -m pytest tests/
```

## License

MIT License