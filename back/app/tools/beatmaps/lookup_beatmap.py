import asyncio
import os

from aiosu.v2.client import Client
from app.models import AIBeatmapsetSearchResponse
from dotenv import load_dotenv
from app.utils.logging import logging_factory
from aiosu.exceptions import APIException, RefreshTokenExpiredError

load_dotenv()
logger = logging_factory(__name__)

limit = (10, 1)
client = Client(
    client_id=os.getenv("OSU_CLIENT_ID"),
    client_secret=os.getenv("OSU_CLIENT_SECRET"),
    limiter=limit
)


async def beatmap_search(query: str, ):
    try:
        response = await client.search_beatmapsets(query=query)
        raw_data = response.model_dump(mode="json", by_alias=True)
        result = AIBeatmapsetSearchResponse.model_validate(raw_data)

        await client.aclose()
        return result
    except APIException as e:
        logger.error(f"api call failed: {str(e)}")
        await client.aclose()
        raise
    except RefreshTokenExpiredError as e:
        logger.error(f"expired token: {str(e)}")
        await client.aclose()
        raise
    except Exception as e:
        logger.error(f"error occured: {str(e)}")
        await client.aclose()
        raise
