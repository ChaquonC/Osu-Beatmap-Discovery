import pytest
import pytest_asyncio

from app.tools.tool_registry import tool_registry
from app.core.companies.openai import OpenAIAdapter
from unittest.mock import AsyncMock
from openai.types.responses import Response
from app.models import LLMResponse, ToolCall


@pytest.mark.asyncio
async def test_format_tools():
    adapter = OpenAIAdapter(api_key="")

    formated_tools = adapter.format_tools(tool_registry.tools)

    assert isinstance(formated_tools, list)
    for tool in formated_tools:
        assert isinstance(tool, dict)
        assert tool["type"] == "function"
        assert isinstance(tool["name"], str)
        assert isinstance(tool["description"], str)
        assert isinstance(tool["parameters"], dict)


@pytest.mark.asyncio
async def test_send(openai_example_response):
    adapter = OpenAIAdapter(api_key="")

    adapter.client.responses.create = AsyncMock(
        return_value=Response.model_validate(openai_example_response)
    )

    result = await adapter.send(tools=tool_registry.tools, input_list=[])

    assert isinstance(result, Response)
    assert adapter.formatted_tools is not None


@pytest.mark.asyncio
async def test_parse_response(openai_example_response):
    adapter = OpenAIAdapter(api_key="")

    response = Response.model_validate(openai_example_response)

    result = adapter.parse_response(response)

    assert isinstance(result, LLMResponse)
    assert result.id == openai_example_response["id"]
    assert result.status == openai_example_response["status"]
    assert result.error == openai_example_response["error"]
    assert result.model == openai_example_response["model"]
    assert result.output == openai_example_response["output"]
    assert result.usage == openai_example_response["usage"]


@pytest.mark.asyncio
async def test_parse_tool_call(openai_example_tool_calls):
    adapter = OpenAIAdapter(api_key="")

    for tool in openai_example_tool_calls:
        result = adapter.parse_tool_call(tool)
        assert isinstance(result, ToolCall)
        assert result.name == tool["name"]
        assert result.inputs == tool["arguments"]

