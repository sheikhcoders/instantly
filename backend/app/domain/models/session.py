from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Session(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[Message] = []
    status: str = "active" # e.g., active, archived, error
    metadata: Optional[dict] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}
