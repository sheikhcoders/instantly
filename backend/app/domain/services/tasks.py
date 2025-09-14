"""
Task and session management service.
"""

from datetime import datetime
from typing import Dict, List, Optional
import redis.asyncio as redis
from app.core.config import settings
from app.domain.models.base import Task, Session, ToolType, Language

class TaskService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    async def create_task(
        self,
        user_id: str,
        title: str,
        description: str,
        tools: List[ToolType],
        language: Language
    ) -> Task:
        """Create a new task."""
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            status="created",
            tools=tools,
            language=language
        )
        await task.insert()
        return task

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        return await Task.get(task_id)

    async def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status."""
        task = await self.get_task(task_id)
        if task:
            task.status = status
            task.updated_at = datetime.utcnow()
            await task.save()
            return True
        return False

    async def create_session(self, task_id: str) -> Session:
        """Create a new session for a task."""
        session = Session(
            task_id=task_id,
            conversation_history=[],
            tool_states={},
            file_uploads=[]
        )
        await session.insert()
        return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        return await Session.get(session_id)

    async def add_conversation_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Add a message to the conversation history."""
        session = await self.get_session(session_id)
        if session:
            session.conversation_history.append({
                "role": role,
                "content": content,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat()
            })
            session.last_active = datetime.utcnow()
            await session.save()
            return True
        return False

    async def update_tool_state(
        self,
        session_id: str,
        tool_type: ToolType,
        state: Dict
    ) -> bool:
        """Update tool state in session."""
        session = await self.get_session(session_id)
        if session:
            session.tool_states[tool_type] = {
                **session.tool_states.get(tool_type, {}),
                **state,
                "updated_at": datetime.utcnow().isoformat()
            }
            session.last_active = datetime.utcnow()
            await session.save()
            return True
        return False