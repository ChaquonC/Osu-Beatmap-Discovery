from app.models import AIBeatmapsetSearchResponse, BeatmapSearchQuery
from dotenv import load_dotenv
from app.utils import ToolError, InvalidRequest, logging_factory
from aiosu.exceptions import APIException, RefreshTokenExpiredError
from app.utils.resources import osu_client

load_dotenv()
logger = logging_factory(__name__)


async def beatmap_search(search: BeatmapSearchQuery) -> AIBeatmapsetSearchResponse:
    try:

        if not search.query:
            raise InvalidRequest("Search must include 'query'")

        normalized_search = search.model_dump(exclude_none=True)

        response = await osu_client.search_beatmapsets(**normalized_search)
        raw_data = response.model_dump(mode="json", by_alias=True)
        result = AIBeatmapsetSearchResponse.model_validate(raw_data)

        return result
    except APIException as e:
        logger.info(f"api call failed: {str(e)}")
        raise ToolError(message="api call failed")
    except RefreshTokenExpiredError as e:
        logger.info(f"expired token: {str(e)}")
        raise ToolError(message="expired api token could not be refreshed")
    except Exception as e:
        logger.info(f"error occured: {str(e)}")
        raise ToolError(message=str(e))
