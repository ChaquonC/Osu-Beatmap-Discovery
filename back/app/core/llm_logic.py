from app.models import ClientRequest
from app.utils import InvalidRequest, logging_factory
from app.core.llm_proxy import LLMProxy
from app.tools.tool_registry import tool_registry
from typing import Any

logger = logging_factory(__name__)


def agent_levels(agent_code: str):
    switch = {
        "thinking_on_a_budget": 1,
        "basic": 3,
        "hes_cooking": 5,
        "the_thinker": 8
    }
    # I want it to throw an error in case future Chaquon messes up :)
    return switch[agent_code]


async def call_agent(request: ClientRequest) -> list[dict[str, Any]]:
    try:
        logger.info(f"running {request.model_type} agent at '{request.thinking_level}' thinking level")
        client = LLMProxy(company=request.model_type, tools=tool_registry)

        if request.existing_conversation:
            conversation = request.existing_conversation
        else:
            conversation = [{"role": "user", "content": request.prompt}]

        agent_turns = agent_levels(request.thinking_level)

        logger.info(f"running {agent_turns} thinking loops")
        for _ in range(agent_turns):
            response = await client.send_prompt(inputs=conversation)

            normalized_response = client.parse_response(response)

            for action in normalized_response.output:
                if action["type"] == client.action_type.TOOL_CALL:
                    task = {"role": "assistant", "content": f"assistant called {action["name"]} tool"}
                    logger.info(f"running {task}")
                    conversation.append(task)
                    tool_call = client.parse_tool_call(action)
                    tool_info = tool_registry.tools.get(tool_call.name)
                    tool_response = await tool_info.fn(**tool_call.inputs)
                    conversation.append({"role": "developer", "content": tool_response})
                elif action["type"] == client.action_type.OUTPUT_TEXT:
                    conversation.append({"role": "assistant", "content": action["text"]})

        logger.info("returning conversation")
        return conversation
    except InvalidRequest:
        raise
    except Exception as e:
        logger.info(f"error occured: {str(e)}")
        raise e
