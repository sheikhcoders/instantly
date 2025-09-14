from pydantic import BaseModel, Field
from typing import Dict, Any, List, Literal

class Tool(BaseModel):
    name: str = Field(..., description="The name of the tool.")
    description: str = Field(..., description="A brief description of what the tool does.")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="JSON schema for the tool's input parameters.")

class ToolOutput(BaseModel):
    tool_name: str
    output: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ToolCall(BaseModel):
    tool_name: str
    tool_input: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    output: Optional[ToolOutput] = None
