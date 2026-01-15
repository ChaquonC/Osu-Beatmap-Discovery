from typing import Any
from app.core.companies.template import BaseLLMAdapter
from openai import AsyncOpenAI
from app.models import Tool, LLMResponse, LLMActionType


class OpenAIAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.formatted_tools = None

    def format_tools(self, tools: dict[str, Tool]) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_modelmodel_json_schema()
            }
            for tool in tools.values()
        ]

    async def send(self, tools: dict[str, Tool], input_list: list[dict[str, str]]) -> Any:
        if not self.formatted_tools:
            self.formatted_tools = self.format_tools(tools)
        response = await self.client.responses.create(
            model="",
            tools=self.formatted_tools,
            input=input_list
        )
        return response

    def parse_response(self, response: dict[str, Any]) -> LLMResponse:
        # implement later
        pass
