import asyncio
import os
from aiosu.v2.client import Client
from aiosu.models.beatmap import Beatmapset, BeatmapsetSearchResponse

from dotenv import load_dotenv

load_dotenv()

limit = (10, 1)
client = Client(
    client_id=os.getenv("OSU_CLIENT_ID"),
    client_secret=os.getenv("OSU_CLIENT_SECRET"),
    limiter=limit
)


async def beatmap_search(query: str, ):
    try:
        response = await client.search_beatmapsets(query=query)
        beatmaps = response.beatmapsets
        '''
        Notes for implementation:
        beatmaps is a list of Beatmapset objects
        to-do: 
        - Make a model with descriptions so the agent knows the ins and outs of beatmapset (Will have to do the same for
        beatmap and the other nested models) using inheritance, just add descriptions
        - map the raw data to my descriptive model and dump that as return
        
        example:
        raw = beatmapset.model_dump(mode="json", by_alias=True)
        result = BeatmapsetResult.model_validate(raw)
        return result.model_dump(mode="json", by_alias=True, exclude_none=True)
        '''

        await client.aclose()
    except:
        await client.aclose()
        raise


asyncio.run(beatmap_search(query="miku"))
