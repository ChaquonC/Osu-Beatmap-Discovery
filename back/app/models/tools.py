from pydantic import BaseModel
from typing import Callable, Any, Optional, Literal
from enum import Enum


class Tool(BaseModel):
    name: str
    description: str
    fn: Callable
    input_model: type[BaseModel]


class ToolRegistry(BaseModel):
    tools: dict[str, Tool]


class OpenAIActionType(Enum):
    TOOL_CALL = "function_call"
    OUTPUT_TEXT = "message"


class AnthropicActionType(Enum):
    TOOL_CALL = "tool_use"
    OUTPUT_TEXT = "text"


class LLMResponse(BaseModel):
    id: str
    output: list[dict]
    model: str
    usage: dict[str, Any]
    status: Optional[str] = None
    error: Optional[str] = None


class ToolCall(BaseModel):
    name: str
    inputs: dict

class Message(BaseModel):
    role: Literal["user", "assistant", "system", "tool"]
    content: str

class Conversation(BaseModel):
    conversation: list[Message]
