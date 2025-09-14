from typing import List, Any, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, AIMessage, ChatResult, ChatGeneration
from instantly import GoogleAIClient, OpenAIClient

class InstantlyChat(BaseChatModel):
    """
    A LangChain-compatible chat model that wraps the Instantly clients.
    """
    client: Any
    model: str

    def __init__(self, client: Any, model: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.client = client
        self.model = model

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Generates a chat completion for the given messages.
        """
        message_dicts = [{"role": "user" if msg.type == "human" else msg.type, "content": msg.content} for msg in messages]
        response = self.client.chat_completion(
            model=self.model,
            messages=message_dicts,
            **kwargs,
        )
        content = response["choices"][0]["message"]["content"]
        message = AIMessage(content=content)
        return ChatResult(generations=[ChatGeneration(message=message)])

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "instantly_chat"

class InstantlyGoogleChat(InstantlyChat):
    """
    A LangChain-compatible chat model that wraps the Instantly GoogleAIClient.
    """
    def __init__(self, model: str, **kwargs: Any):
        client = GoogleAIClient(**kwargs)
        super().__init__(client=client, model=model, **kwargs)

class InstantlyOpenAIChat(InstantlyChat):
    """
    A LangChain-compatible chat model that wraps the Instantly OpenAIClient.
    """
    def __init__(self, model: str, **kwargs: Any):
        client = OpenAIClient(**kwargs)
        super().__init__(client=client, model=model, **kwargs)
