from pydantic import BaseModel
from typing import Callable, Any, Optional
from enum import Enum, auto


class Tool(BaseModel):
    name: str
    description: str
    fn: Callable
    input_model: type[BaseModel]


class ToolRegistry(BaseModel):
    tools: dict[str, Tool]


class LLMActionType(Enum):
    TOOL_CALL = auto()
    OUTPUT_TEXT = auto()
    STRUCTURED_OUTPUT = auto()

class LLMResponse(BaseModel):
    id: str
    output: list[dict]
    model: str
    role: str
    usage: dict[str, Any]
    context_to_add: Optional[dict[str, str]] = None

