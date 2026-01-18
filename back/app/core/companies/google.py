from typing import Any
from google.genai import Client, types
from app.core.companies.template import BaseLLMAdapter
from app.models import Tool, LLMResponse


class GoogleAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str):
        self.client = Client(api_key=api_key).aio
        self.formatted_tools = None

    def format_tools(self, tools: dict[str, Tool]) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_model.model_json_schema()
            }
            for tool in tools.values()
        ]

    async def send(self, tools: dict[str, Tool], input_list: list[dict[str, str]]) -> Any:
        if not self.formatted_tools:
            self.formatted_tools = self.format_tools(tools)
        formatted_inputs = []
        for message in input_list:
            formatted_inputs.append(types.Content(
                role=message["role"], parts=[types.Part(text=message["content"])]
            ))
        config = types.GenerateContentConfig(tools=tools)

        response = await self.client.models.generate_content(
            model="",
            contents=formatted_inputs,
            config=config
        )
        return response

    def parse_response(self, response: types.GenerateContentResponse) -> LLMResponse:
        # will revisit, google documentation is confusing
        pass
