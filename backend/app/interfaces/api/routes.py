from fastapi import APIRouter, HTTPException, status
from typing import List
from backend.app.application.schemas.session import SessionCreate, SessionResponse
from backend.app.domain.services.session_service import session_service
from backend.app.application.services.conversation_service import conversation_service
from backend.app.domain.models.session import Message
from sse_starlette.sse import EventSourceResponse
import asyncio

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_session(session_create: SessionCreate):
    session = await session_service.create_session(session_create.user_id, session_create.initial_message)
    return session

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session_by_id(session_id: str):
    session = await session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return session

@router.get("/", response_model=List[SessionResponse])
async def get_all_user_sessions(user_id: str):
    sessions = await session_service.get_all_sessions(user_id)
    return sessions

@router.post("/{session_id}/message")
async def send_message_to_session(session_id: str, message: str):
    session = await session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    user_message = Message(role="user", content=message)
    await session_service.add_message_to_session(session_id, user_message)

    async def event_generator():
        async for chunk in conversation_service.generate_response(session):
            yield {"event": "new_message", "data": chunk}
        yield {"event": "end_of_stream", "data": ""}

    return EventSourceResponse(event_generator())

@router.get("/health")
async def health_check():
    return {"status": "ok"}
