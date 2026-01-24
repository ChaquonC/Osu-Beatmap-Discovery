from typing import Any
from app.core.companies.template import BaseLLMAdapter
from anthropic import AsyncAnthropic, types

from app.models import Tool, AnthropicActionType, LLMResponse, ToolCall
from app.utils import logging_factory

logger = logging_factory(__name__)


class AnthropicAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.formatted_tools = None
        self.action_type = AnthropicActionType

    def format_tools(self, tools: dict[str, Tool]) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_model.model_json_schema()
            }
            for tool in tools.values()
        ]

    async def send(self, tools: dict[str, Tool], input_list: list[dict[str, str]]) -> types.Message:
        if not self.formatted_tools:
            self.formatted_tools = self.format_tools(tools)
        response = await self.client.messages.create(
            model="",
            messages=input_list,
            tools=self.formatted_tools,
            max_tokens=100
        )
        return response

    def parse_response(self, response: types.Message) -> LLMResponse:
        response_dict = response.model_dump()
        normalized_response = LLMResponse(
            id=response_dict.get("id"),
            output=response_dict.get("content"),
            model=response_dict.get("model"),
            usage=response_dict.get("usage"),
        )

        logger.info(f"parsed response: {normalized_response}")
        return normalized_response

    def parse_tool_call(self, arguments: dict[str, str]) -> ToolCall:
        return ToolCall(
            name=arguments.get("name"),
            inputs=arguments.get("input"),
        )
