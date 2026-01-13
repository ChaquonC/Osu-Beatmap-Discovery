import os
from typing import Optional
from aiosu.v2 import Client

osu_client: Optional[Client] = None

def init_osu_client() -> Client:
    global osu_client
    if osu_client is None:
        # 10 requests per second
        limit = (10, 1)
        osu_client = Client(
            client_id=os.getenv("OSU_CLIENT_ID"),
            client_secret=os.getenv("OSU_CLIENT_SECRET"),
            limiter=limit,
        )
    return osu_client

async def close_osu_client():
    global osu_client
    if osu_client is not None:
        await osu_client.aclose()
        osu_client = None