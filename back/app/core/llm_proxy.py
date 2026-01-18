import os

from app.models.tools import Tool
from app.core.companies.openai import OpenAIAdapter
from app.core.companies.google import GoogleAdapter
from app.core.companies.anthropic import AnthropicAdapter
from dotenv import load_dotenv
from typing import Any
from app.models import LLMResponse, ToolCall

load_dotenv()


class LLMProxy:
    def __init__(self, company: str, tools: dict[str, Tool]):
        switch = {
            "openai": OpenAIAdapter(api_key=os.getenv("OPENAI_API_KEY")),
            "anthropic": AnthropicAdapter(api_key=os.getenv("ANTHROPIC_API_KEY")),
            "google": GoogleAdapter(api_key=os.getenv("GOOGLE_API_KEY"))
        }
        self.adapter = switch[company]
        self.tools = tools
        self.action_type = self.adapter.action_type

    async def send_prompt(self, inputs: list[dict[str, str]]) -> Any:
        await self.adapter.send(tools=self.tools, input_list=inputs)

    def parse_response(self, response) -> LLMResponse:
        return self.adapter.parse_response(response)

    def parse_tool_call(self, arguments: dict[str, str]) -> ToolCall:
        return self.adapter.parse_tool_call(arguments)
