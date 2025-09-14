import asyncio
from typing import AsyncGenerator
from backend.app.domain.models.session import Message, Session
from backend.app.domain.services.session_service import session_service
from backend.app.infrastructure.config import settings
import openai

class ConversationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def generate_response(self, session: Session) -> AsyncGenerator[str, None]:
        messages = [{"role": msg.role, "content": msg.content} for msg in session.messages]

        try:
            response_stream = await openai.ChatCompletion.acreate(
                model="gpt-4", # Or another suitable model
                messages=messages,
                stream=True
            )

            full_response_content = ""
            async for chunk in response_stream:
                content = chunk.choices[0].delta.get("content")
                if content:
                    full_response_content += content
                    yield content
            
            # Save the full AI response to the session
            ai_message = Message(role="assistant", content=full_response_content)
            await session_service.add_message_to_session(session.id, ai_message)

        except Exception as e:
            print(f"Error generating response: {e}")
            yield f"Error: Could not generate response. {e}"

conversation_service = ConversationService()
