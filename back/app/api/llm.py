from fastapi import APIRouter
from http import HTTPStatus
from typing import Any
from app.utils.logging import getLogger

logger = getLogger(__name__)

llm_router = APIRouter(prefix="/api/v1/llm", tags=["LLM Endpoints"])


@llm_router.post("/agent",
                    status_code=HTTPStatus.OK,
                    description="Sends a request to agent",
                    responses={},
                    response_model={},
                    dependencies=[],
                    )
async def call_agent(request: dict[str, Any]):
    try:
        print("do something")
    except Exception:
        pass


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
