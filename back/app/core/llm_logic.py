from app.models import ClientRequest, LLMActionType
from app.utils import InvalidRequest, logging_factory
from app.core.llm_proxy import LLMProxy
from app.tools.tool_registry import tool_registry

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


async def call_agent(request: ClientRequest):
    try:
        logger.info(f"running {request.model_type} agent at '{request.thinking_level}' thinking level")
        client = LLMProxy(company=request.model_type, tools=tool_registry)

        conversation = request.existing_conversation or [{"role": "user", "content": request.prompt}]

        agent_turns = agent_levels(request.thinking_level)

        logger.info(f"running {agent_turns} thinking loops")
        for _ in range(agent_turns):
            response = await client.send_prompt(inputs=conversation)

            normalized_response = client.parse_response(response)

            conversation.append(normalized_response.context_to_add)

            for action in normalized_response.output:
                if action["type"] == LLMActionType.TOOL_CALL:
                    # implement later
                    pass
                elif action["type"] == LLMActionType.OUTPUT_TEXT:
                    # implement later
                    pass
                elif action["type"] == LLMActionType.STRUCTURED_OUTPUT:
                    # implement later
                    pass

        final_response = conversation[-1]

        logger.info("returning agent final response")
        # should probably validate final response again

        return final_response
    except InvalidRequest:
        raise
    except Exception as e:
        logger.info(f"error occured: {str(e)}")
