from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class MessageSchema(BaseModel):
    role: str
    content: str
    timestamp: datetime

class SessionCreate(BaseModel):
    user_id: str
    initial_message: Optional[str] = None

class SessionResponse(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageSchema]
    status: str
    metadata: Optional[dict] = None

    class Config:
        orm_mode = True
