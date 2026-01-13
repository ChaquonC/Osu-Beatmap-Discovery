import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastmcp import FastMCP
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.utils import logging_factory, register_tools
from app.api.llm import llm_router
from app.utils.resources import init_osu_client, close_osu_client
from app.tools.tool_registry import tools

load_dotenv()
logger = logging_factory(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    logger.info("********** STARTING APPLICATION **********")
    init_osu_client()
    try:
        yield
    finally:
        logger.info("********** SHUTTING DOWN APPLICATION **********")
        await close_osu_client()
        logger.info("********** APPLICATION SHUTDOWN COMPLETE **********")


app = FastAPI(
    title="Osu Beatmap Discovery",
    lifespan=lifespan
)

app.include_router(llm_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id", "mcp-session-id"],
)

mcp = FastMCP.from_fastapi(app=app, name="Beatmap-Discovery-Tools")

register_tools(tools=tools, mcp=mcp)

mcp_app = mcp.http_app(path="/mcp")


@asynccontextmanager
async def combined_lifespan(app_instance: FastAPI):
    async with lifespan(app_instance):
        async with mcp_app.lifespan(app_instance):
            yield


combined_app = FastAPI(
    title="Osu Beatmap Discovery with MCP",
    routes=[
        *mcp_app.routes,
        *app.routes
    ],
    lifespan=combined_lifespan
)


@app.get("/swagger-ui/index.html", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("app.main:combined_app", host="0.0.0.0", port=8000)
