import pytest


@pytest.fixture
def openai_example_response():
    return {
        "id": "resp_67ccd2bed1ec8190b14f964abc0542670bb6a6b452d3795b",
        "object": "response",
        "created_at": 1741476542,
        "status": "completed",
        "completed_at": 1741476543,
        "error": None,
        "incomplete_details": None,
        "instructions": None,
        "max_output_tokens": None,
        "model": "gpt-4.1-2025-04-14",
        "output": [
            {
                "type": "message",
                "id": "msg_67ccd2bf17f0819081ff3bb2cf6508e60bb6a6b452d3795b",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": "In a peaceful grove beneath a silver moon, a unicorn named Lumina discovered a hidden pool that reflected the stars. As she dipped her horn into the water, the pool began to shimmer, revealing a pathway to a magical realm of endless night skies. Filled with wonder, Lumina whispered a wish for all who dream to find their own hidden magic, and as she glanced back, her hoofprints sparkled like stardust.",
                        "annotations": [],
                        "logprobs": None
                    }
                ]
            }
        ],
        "parallel_tool_calls": True,
        "previous_response_id": None,
        "reasoning": {
            "effort": None,
            "summary": None
        },
        "store": True,
        "temperature": 1.0,
        "text": {
            "format": {
                "type": "text"
            }
        },
        "tool_choice": "auto",
        "tools": [],
        "top_p": 1.0,
        "truncation": "disabled",
        "usage": {
            "input_tokens": 36,
            "input_tokens_details": {
                "cached_tokens": 0
            },
            "output_tokens": 87,
            "output_tokens_details": {
                "reasoning_tokens": 0
            },
            "total_tokens": 123
        },
        "user": None,
        "metadata": {}
    }


@pytest.fixture
def openai_example_tool_calls():
    return [
        {
            "id": "fc_12345xyz",
            "call_id": "call_12345xyz",
            "type": "function_call",
            "name": "get_weather",
            "arguments": {"location": "Paris, France"}
        },
        {
            "id": "fc_67890abc",
            "call_id": "call_67890abc",
            "type": "function_call",
            "name": "get_weather",
            "arguments": {"location": "Bogotá, Colombia"}
        },
        {
            "id": "fc_99999def",
            "call_id": "call_99999def",
            "type": "function_call",
            "name": "send_email",
            "arguments": {"to": "bob@email.com", "body": "Hi bob"}
        }
    ]


@pytest.fixture
def anthropic_example_response():
    return {
        "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
        "content": [
            {
                "citations": [
                    {
                        "cited_text": "cited_text",
                        "document_index": 0,
                        "document_title": "document_title",
                        "end_char_index": 0,
                        "file_id": "file_id",
                        "start_char_index": 0,
                        "type": "char_location"
                    }
                ],
                "text": "Hi! My name is Claude.",
                "type": "text"
            }
        ],
        "model": "claude-sonnet-4-5-20250929",
        "role": "assistant",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "type": "message",
        "usage": {
            "cache_creation": {
                "ephemeral_1h_input_tokens": 0,
                "ephemeral_5m_input_tokens": 0
            },
            "cache_creation_input_tokens": 2051,
            "cache_read_input_tokens": 2051,
            "input_tokens": 2095,
            "output_tokens": 503,
            "server_tool_use": {
                "web_search_requests": 0
            },
            "service_tier": "standard"
        }
    }


@pytest.fixture
def anthropic_example_tool_calls():
    return [
        {
            "type": "tool_use",
            "id": "toolu_abc123",
            "name": "query_database",
            "input": {"sql": "<sql>"},
            "caller": {"type": "direct"}
        },
        {
            "type": "tool_use2",
            "id": "toolu_abc123",
            "name": "query_database",
            "input": {"sql": "<sql>"},
            "caller": {"type": "direct"}
        }
    ]