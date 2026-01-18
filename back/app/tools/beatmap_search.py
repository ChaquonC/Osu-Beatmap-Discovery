from app.models import AIBeatmapsetSearchResponse, BeatmapSearchQuery
from app.utils import ToolError, InvalidRequest, logging_factory, ok, fail
from aiosu.exceptions import APIException, RefreshTokenExpiredError
from app.utils.resources import osu_client

logger = logging_factory(__name__)


async def beatmap_search(search: BeatmapSearchQuery) -> AIBeatmapsetSearchResponse:
    try:

        if not search.query:
            raise InvalidRequest("Search must include 'query'")

        logger.info(f"Looking for beatmaps; query: f{search.query}")

        normalized_search = search.model_dump(exclude_none=True)

        response = await osu_client.search_beatmapsets(**normalized_search)
        raw_data = response.model_dump(mode="json", by_alias=True)
        result = AIBeatmapsetSearchResponse.model_validate(raw_data)

        logger.info(f"retrieved data from osu api")

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


async def beatmap_search_tool(search: dict) -> dict:
    try:
        logger.info("starting beatmap search tool call")

        search = BeatmapSearchQuery(**search)

        result = await beatmap_search(search)
        raw_data = result.model_dump(mode="json", by_alias=True, exclude_none=True)

        if len(raw_data) == 0:
            logger.info("beatmap search tool returned nothing")
            return fail(code=404, message="Search resulted in no beatmap sets returned")

        logger.info("beatmap search tool successful")
        return ok(raw_data)
    except InvalidRequest as e:
        logger.info("beatmap search tool failed")
        raise ToolError(code=400, message=f"Invalid Request: {str(e)}")
    except Exception as e:
        logger.info("beatmap search tool failed")
        raise ToolError(code=500, message=str(e))
