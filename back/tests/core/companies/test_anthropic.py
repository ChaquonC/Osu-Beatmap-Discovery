import pytest
import pytest_asyncio

from app.tools.tool_registry import tool_registry
from app.core.companies.anthropic import AnthropicAdapter
from unittest.mock import AsyncMock
from anthropic.types import Message
from app.models import LLMResponse, ToolCall


@pytest.mark.asyncio
async def test_format_tools():
    adapter = AnthropicAdapter(api_key="")

    formated_tools = adapter.format_tools(tool_registry.tools)

    assert isinstance(formated_tools, list)
    for tool in formated_tools:
        assert isinstance(tool, dict)
        assert tool["type"] == "function"
        assert isinstance(tool["name"], str)
        assert isinstance(tool["description"], str)
        assert isinstance(tool["input_schema"], dict)


@pytest.mark.asyncio
async def test_send(anthropic_example_response):
    adapter = AnthropicAdapter(api_key="")

    adapter.client.messages.create = AsyncMock(
        return_value=Message.model_validate(anthropic_example_response)
    )

    result = await adapter.send(tools=tool_registry.tools, input_list=[])

    assert isinstance(result, Message)
    assert adapter.formatted_tools is not None


@pytest.mark.asyncio
async def test_parse_response(anthropic_example_response):
    adapter = AnthropicAdapter(api_key="")

    response = Message.model_validate(anthropic_example_response)

    result = adapter.parse_response(response)

    assert isinstance(result, LLMResponse)
    assert result.id == anthropic_example_response["id"]
    assert result.status is None
    assert result.error is None
    assert result.model == anthropic_example_response["model"]
    assert result.output == anthropic_example_response["content"]
    assert result.usage == anthropic_example_response["usage"]


@pytest.mark.asyncio
async def test_parse_tool_call(anthropic_example_tool_calls):
    adapter = AnthropicAdapter(api_key="")

    for tool in anthropic_example_tool_calls:
        result = adapter.parse_tool_call(tool)
        assert isinstance(result, ToolCall)
        assert result.name == tool["name"]
        assert result.inputs == tool["input"]

