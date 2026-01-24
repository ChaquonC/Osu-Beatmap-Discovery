from fastapi import APIRouter
from http import HTTPStatus
from typing import Any
from app.utils.logging import getLogger
from app.core.llm_logic import call_agent
from app.models import ClientRequest, APIResponseModel

logger = getLogger(__name__)

llm_router = APIRouter(prefix="/api/v1/llm", tags=["LLM Endpoints"])


@llm_router.post("/agent",
                 status_code=HTTPStatus.OK,
                 description="Sends a conversation prompt to an agent",
                 response_model=APIResponseModel,
                 dependencies=[],
                 )
async def call_agent(request: ClientRequest):
    try:
        client_request = ClientRequest.model_validate(request)

        logger.info(f"calling agent with the prompt {client_request.prompt} with {client_request.model_type} agent")

        conversation = await call_agent(client_request)

        return conversation.model_dump()
    except Exception as e:
        logger.info(f"error occurred: {str(e)}")


@llm_router.post("/single-call",
                 status_code=HTTPStatus.OK,
                 description="Sends a single request to llm",
                 responses={},
                 response_model={},
                 dependencies=[],
                 )
async def llm_call(request: dict[str, Any]):
    try:
        print("do something")
    except Exception:
        pass
