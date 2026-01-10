import os
import asyncio

from aiosu.v2.client import Client
from app.models import AIBeatmapsetSearchResponse, BeatmapSearchQuery
from dotenv import load_dotenv
from app.utils import ToolError, InvalidRequest, logging_factory
from aiosu.exceptions import APIException, RefreshTokenExpiredError

load_dotenv()
logger = logging_factory(__name__)

limit = (10, 1)
client = Client(
    client_id=os.getenv("OSU_CLIENT_ID"),
    client_secret=os.getenv("OSU_CLIENT_SECRET"),
    limiter=limit
)


async def beatmap_search(search: BeatmapSearchQuery) -> AIBeatmapsetSearchResponse:
    try:
        if not search.query:
            raise InvalidRequest("Search must include 'query'")

        normalized_search = search.model_dump(exclude_none=True)

        response = await client.search_beatmapsets(**normalized_search)
        raw_data = response.model_dump(mode="json", by_alias=True)
        result = AIBeatmapsetSearchResponse.model_validate(raw_data)

        await client.aclose()
        return result
    except APIException as e:
        logger.info(f"api call failed: {str(e)}")
        await client.aclose()
        raise ToolError(message="api call failed")
    except RefreshTokenExpiredError as e:
        logger.info(f"expired token: {str(e)}")
        await client.aclose()
        raise ToolError(message="expired api token could not be refreshed")
    except Exception as e:
        logger.info(f"error occured: {str(e)}")
        await client.aclose()
        raise ToolError(message=str(e))

if __name__ == "__main__":
    r = asyncio.run(beatmap_search(BeatmapSearchQuery(query="Hatsune Miku")))
    print(r.beatmapsets[0])