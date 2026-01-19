from typing import Any
from app.core.companies.template import BaseLLMAdapter
from openai import AsyncOpenAI
from app.models import Tool, LLMResponse, OpenAIActionType, ToolCall
from app.utils import logging_factory
from openai.types.responses.response import Response

logger = logging_factory(__name__)


class OpenAIAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.formatted_tools = None
        self.action_type = OpenAIActionType

    def format_tools(self, tools: dict[str, Tool]) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_model.model_json_schema()
            }
            for tool in tools.values()
        ]

    async def send(self, tools: dict[str, Tool], input_list: list[dict[str, str]]) -> Response:
        if not self.formatted_tools:
            self.formatted_tools = self.format_tools(tools)
        response = await self.client.responses.create(
            model="",
            tools=self.formatted_tools,
            input=input_list
        )
        return response

    def parse_response(self, response: Response) -> LLMResponse:
        response_dict = response.model_dump()
        normalized_response = LLMResponse(
            id=response_dict.get("id"),
            status=response_dict.get("status"),
            error=response_dict.get("error"),
            model=response_dict.get("model"),
            output=response_dict.get("output"),
            usage=response_dict.get("usage"),
        )

        logger.info(f"parsed response: {normalized_response}")
        return normalized_response

    def parse_tool_call(self, tool_call: dict) -> ToolCall:
        return ToolCall(
            name=tool_call.get("name"),
            inputs=tool_call.get("arguments"),
        )
