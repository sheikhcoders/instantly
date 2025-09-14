from typing import List, Optional
from uuid import uuid4
from backend.app.domain.models.session import Session, Message
from backend.app.infrastructure.database import db

class SessionService:
    def __init__(self):
        self.collection = db.client.get_database("instantly").get_collection("sessions")

    async def create_session(self, user_id: str, initial_message: Optional[str] = None) -> Session:
        session_id = str(uuid4())
        messages = []
        if initial_message:
            messages.append(Message(role="user", content=initial_message))

        session = Session(_id=session_id, user_id=user_id, messages=messages)
        await self.collection.insert_one(session.dict(by_alias=True))
        return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        session_data = await self.collection.find_one({"_id": session_id})
        if session_data:
            return Session.parse_obj(session_data)
        return None

    async def add_message_to_session(self, session_id: str, message: Message) -> Optional[Session]:
        await self.collection.update_one(
            {"_id": session_id},
            {"$push": {"messages": message.dict()}, "$set": {"updated_at": message.timestamp}}
        )
        return await self.get_session(session_id)

    async def get_all_sessions(self, user_id: str) -> List[Session]:
        sessions_data = await self.collection.find({"user_id": user_id}).to_list(length=100)
        return [Session.parse_obj(s) for s in sessions_data]

session_service = SessionService()
