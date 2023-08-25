from os import getenv
import aiohttp
from typing import Literal


class API:
    API_URL = f"{getenv('BABYFALCON_URL')}/gpt"

    ENDPOINTS_ALIASES = Literal[
        "chat_completion",
    ]

    API_ENDPOINTS = {
        "chat_completion": "/chat-compeltion/",
    }

    @classmethod
    def get_url(cls, endpoint_name: ENDPOINTS_ALIASES):
        return cls.API_URL + cls.API_ENDPOINTS.get(endpoint_name)


async def chat_completion(user_id: int, query: str):

    async with aiohttp.ClientSession() as session:
        async with session.post(API.get_url('chat_completion'), json={"id": user_id, "query": query}) as response:
            response_data = await response.json()
            return response_data["answer"]
