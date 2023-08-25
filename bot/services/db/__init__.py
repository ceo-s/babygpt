from os import getenv
import aiohttp
from typing import Literal, Any
from pydantic import BaseModel, Json

from . import models as M


class API:
    API_URL = f"{getenv('BABYFALCON_URL')}/db"

    ENDPOINTS_ALIASES = Literal[
        "auth_user",
        "get_user_data",
        "update_user_data",
        "update_documents",
    ]

    API_ENDPOINTS = {
        "auth_user": "/auth-user/",
        "get_user_data": "/get-user-data/",
        "update_user_data": "/update-user-data/",
        "update_documents": "/update-documents/",
    }

    @classmethod
    def get_url(cls, endpoint_name: ENDPOINTS_ALIASES):
        return cls.API_URL + cls.API_ENDPOINTS.get(endpoint_name)


async def authenticate_user(user: M.User) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(API.get_url('auth_user'), json=user.model_dump()) as response:
            response_data = await response.json()
            return response_data["authenticated"]

# USER_ATTRS = Literal[
#     "username",
#     "first_name",
#     "settings",
# ]

# USER_SETTINGS_ATTRS = Literal[
#     "model_temperature",
#     "prompt",
#     "history",
# ]


async def get_user_data(user: M.OUser) -> M.User:
    async with aiohttp.ClientSession() as session:
        async with session.post(API.get_url('get_user_data'), json=user.model_dump()) as response:
            response_data = await response.json()
            return M.User(**response_data)


async def update_user_data(user: M.OUser):
    async with aiohttp.ClientSession() as session:

        async with session.post(API.get_url('update_user_data'), json=user.model_dump()) as response:
            await response.json()


async def update_model_documents(user_id: int, username: str, text: str):

    async with aiohttp.ClientSession() as session:
        async with session.get(API.get_url('update_documents'), params={"user_id": user_id, "username": username, "document_text": text}) as response:
            response_data = await response.json()
            return response_data["succ"]
