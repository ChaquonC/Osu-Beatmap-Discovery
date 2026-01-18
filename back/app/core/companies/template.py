from abc import ABC, abstractmethod
from typing import Any
from app.models import Tool, LLMResponse, ToolCall


class BaseLLMAdapter(ABC):
    @abstractmethod
    def format_tools(self, tools: dict[str, Tool]) -> list[dict[str, Any]]:
        """Convert internal Tool objects into provider-specific tool schema."""
        raise NotImplementedError

    def parse_response(self, response: Any) -> LLMResponse:
        """Converts LLM response into standardized response object"""
        raise NotImplementedError

    @abstractmethod
    async def send(self, tools: dict[str, Tool], input_list: list[dict[str, str]]) -> Any:
        """Send prompt + tools to the provider and return response."""
        raise NotImplementedError

    def parse_tool_call(self, arguments: dict[str, str]) -> ToolCall:
        """Converts specific tool call output to universal tool call object."""
        raise NotImplementedError
