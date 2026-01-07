import os

from httpx import post
from dotenv import load_dotenv

load_dotenv()


def get_client_auth():
    response = post(
        url="https://osu.ppy.sh/oauth/token",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "client_id": os.getenv("OSU_CLIENT_ID"),
            "client_secret": os.getenv("OSU_CLIENT_SECRET"),
            "grant_type": "client_credentials",
            "scope": "public"
        }
    )

    response_dict = response.json()


