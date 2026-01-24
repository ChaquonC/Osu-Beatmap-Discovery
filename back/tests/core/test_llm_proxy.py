import pytest
import pytest_asyncio

from app.tools.tool_registry import tool_registry
from app.core.companies.anthropic import AnthropicAdapter
from app.core.companies.openai import OpenAIAdapter
from app.core.llm_proxy import LLMProxy
from app.models import AnthropicActionType, OpenAIActionType
from unittest.mock import AsyncMock
from anthropic.types import Message
from openai.types.responses import Response
from app.models import LLMResponse, ToolCall


@pytest.mark.asyncio
async def test_init_llm_proxy():
    llm_proxy_instance1 = LLMProxy(company="openai", tools=tool_registry.tools)
    llm_proxy_instance2 = LLMProxy(company="anthropic", tools=tool_registry.tools)

    assert isinstance(llm_proxy_instance1.adapter, OpenAIAdapter)
    assert llm_proxy_instance1.tools == tool_registry.tools
    assert llm_proxy_instance1.action_type is OpenAIActionType

    assert isinstance(llm_proxy_instance2.adapter, AnthropicAdapter)
    assert llm_proxy_instance2.tools == tool_registry.tools
    assert llm_proxy_instance2.action_type is AnthropicActionType

    assert isinstance(llm_proxy_instance1, type(llm_proxy_instance2))


@pytest.mark.asyncio
async def test_send_prompt(anthropic_example_response, openai_example_response):
    llm_proxy_instance1 = LLMProxy(company="openai", tools=tool_registry.tools)
    llm_proxy_instance2 = LLMProxy(company="anthropic", tools=tool_registry.tools)

    llm_proxy_instance1.adapter.client.responses.create = AsyncMock(
        return_value=Response.model_validate(openai_example_response)
    )

    result1 = await llm_proxy_instance1.send_prompt(inputs=[])

    assert isinstance(result1, Response)
    assert llm_proxy_instance1.adapter.formatted_tools is not None

    llm_proxy_instance2.adapter.client.messages.create = AsyncMock(
        return_value=Message.model_validate(anthropic_example_response)
    )

    result2 = await llm_proxy_instance2.send_prompt(inputs=[])

    assert isinstance(result2, Message)
    assert llm_proxy_instance2.adapter.formatted_tools is not None


@pytest.mark.asyncio
async def test_parse_response(anthropic_example_response, openai_example_response):
    llm_proxy_instance1 = LLMProxy(company="openai", tools=tool_registry.tools)
    llm_proxy_instance2 = LLMProxy(company="anthropic", tools=tool_registry.tools)

    response1 = Response.model_validate(openai_example_response)

    result1 = llm_proxy_instance1.parse_response(response1)

    assert isinstance(result1, LLMResponse)
    assert result1.id == openai_example_response["id"]
    assert result1.status == openai_example_response["status"]
    assert result1.error == openai_example_response["error"]
    assert result1.model == openai_example_response["model"]
    assert result1.output == openai_example_response["output"]
    assert result1.usage == openai_example_response["usage"]

    response2 = Message.model_validate(anthropic_example_response)

    result2 = llm_proxy_instance2.parse_response(response2)

    assert isinstance(result2, LLMResponse)
    assert result2.id == anthropic_example_response["id"]
    assert result2.status is None
    assert result2.error is None
    assert result2.model == anthropic_example_response["model"]
    assert result2.output == anthropic_example_response["content"]
    assert result2.usage == anthropic_example_response["usage"]


@pytest.mark.asyncio
async def test_parse_tool_call(anthropic_example_tool_calls, openai_example_tool_calls):
    llm_proxy_instance1 = LLMProxy(company="openai", tools=tool_registry.tools)
    llm_proxy_instance2 = LLMProxy(company="anthropic", tools=tool_registry.tools)

    for tool in openai_example_tool_calls:
        result = llm_proxy_instance1.parse_tool_call(tool)
        assert isinstance(result, ToolCall)
        assert result.name == tool["name"]
        assert result.inputs == tool["arguments"]

    for tool in anthropic_example_tool_calls:
        result = llm_proxy_instance2.parse_tool_call(tool)
        assert isinstance(result, ToolCall)
        assert result.name == tool["name"]
        assert result.inputs == tool["input"]

