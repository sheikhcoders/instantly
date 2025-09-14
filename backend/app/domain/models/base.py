"""
Base models for domain entities.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from beanie import Document
from pydantic import BaseModel, Field

class ToolType(str, Enum):
    TERMINAL = "terminal"
    BROWSER = "browser"
    FILE = "file"
    WEB_SEARCH = "web_search"
    MESSAGING = "messaging"
    MCP = "mcp"

class Language(str, Enum):
    EN = "en"
    ZH = "zh"

class User(Document):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"

class Task(Document):
    user_id: str
    title: str
    description: str
    status: str
    sandbox_id: Optional[str]
    tools: List[ToolType]
    language: Language
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "tasks"

class Session(Document):
    task_id: str
    conversation_history: List[Dict[str, Any]]
    tool_states: Dict[str, Any]
    file_uploads: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "sessions"