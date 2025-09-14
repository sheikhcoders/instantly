import os
import pytest
from instantly import OpenAIClient, InferenceClient, GoogleAIClient
from instantly.exceptions import ConfigurationError


def test_openai_client_requires_api_key():
    with pytest.raises(ConfigurationError):
        OpenAIClient(api_key=None)

def test_inference_client_requires_api_key():
    with pytest.raises(ConfigurationError):
        InferenceClient(api_key=None)

def test_googleai_client_requires_api_key():
    with pytest.raises(ConfigurationError):
        GoogleAIClient(api_key=None)

def test_openai_client_stream_chat_completion():
    if not os.environ.get("HF_TOKEN"):
        pytest.skip("HF_TOKEN not set")
    
    client = OpenAIClient()
    messages = [{"role": "user", "content": "Say hello!"}]
    
    stream = client.stream_chat_completion(
        model="moonshotai/Kimi-K2-Instruct",
        messages=messages,
    )
    
    chunks = list(stream)
    assert len(chunks) > 0
    for chunk in chunks:
        assert isinstance(chunk, dict)
        assert "choices" in chunk
        assert len(chunk["choices"]) > 0
        assert "delta" in chunk["choices"][0]
        assert "content" in chunk["choices"][0]["delta"]

def test_googleai_client_chat_completion():
    if not os.environ.get("GOOGLE_API_KEY"):
        pytest.skip("GOOGLE_API_KEY not set")
    
    client = GoogleAIClient()
    messages = [{"role": "user", "content": "Say hello!"}]
    
    response = client.chat_completion(
        model="gemini-2.5-pro",
        messages=messages,
    )
    
    assert isinstance(response, dict)
    assert "choices" in response
    assert len(response["choices"]) > 0
    assert "message" in response["choices"][0]
    assert "content" in response["choices"][0]["message"]

def test_googleai_client_stream_chat_completion():
    if not os.environ.get("GOOGLE_API_KEY"):
        pytest.skip("GOOGLE_API_KEY not set")
    
    client = GoogleAIClient()
    messages = [{"role": "user", "content": "Say hello!"}]
    
    stream = client.stream_chat_completion(
        model="gemini-2.5-pro",
        messages=messages,
    )
    
    chunks = list(stream)
    assert len(chunks) > 0
    for chunk in chunks:
        assert isinstance(chunk, dict)
        assert "choices" in chunk
        assert len(chunk["choices"]) > 0
        assert "delta" in chunk["choices"][0]
        assert "content" in chunk["choices"][0]["delta"]
