from app.models import ClientRequest, Conversation, Message
from app.utils import InvalidRequest, logging_factory
from app.core.llm_proxy import LLMProxy
from app.tools.tool_registry import tool_registry

logger = logging_factory(__name__)


async def call_agent(request: ClientRequest) -> Conversation:
    try:
        logger.info(f"running {request.model_type} agent at '{request.thinking_level}' thinking level")
        client = LLMProxy(company=request.model_type, tools=tool_registry.tools)

        conversation = request.conversation

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
                conversation.append(
                    {"role": "tool", "content": {"tool_response": tool_response, "developer": "send final response"}})
            elif action["type"] == client.action_type.OUTPUT_TEXT:
                conversation.append({"role": "assistant", "content": action["text"]})

        final_response = await client.send_prompt(inputs=conversation)
        normalized_final_response = client.parse_response(final_response)
        output = normalized_final_response.output[0]
        conversation.append({"role": "assistant", "content": output["text"]})

        logger.info("returning conversation")
        formatted_conversation = Conversation.model_validate(Message.model_validate(m) for m in conversation)
        return formatted_conversation
    except InvalidRequest:
        raise
    except Exception as e:
        logger.info(f"error occured: {str(e)}")
        raise e
