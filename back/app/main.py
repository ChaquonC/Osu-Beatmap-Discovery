import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.utils import logging_factory
from app.api.llm import llm_router
from app.utils.resources import init_osu_client, close_osu_client

load_dotenv()
logger = logging_factory(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
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
        "http://localhost:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/swagger-ui/index.html", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
