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


# async def chat_completion(message: Message) -> str:

#     async with get_sessionmaker().begin() as db_session:
#         db_session: AsyncSession
#         res = await db_session.execute(select(UserSettings).where(
#             UserSettings.user_fk == message.from_user.id))

#         settings = res.scalar_one_or_none()

#         if not settings:
#             raise Exception()

#         json_body = {
#             "name": settings.user.first_name,
#             "query": message.text,
#             "model_temperature": settings.model_temperature,
#             "prompt": settings.prompt,
#             "history": settings.history,
#         }

#     print(json_body)
#     async with aiohttp.ClientSession() as session:
#         async with session.post(API.get_url("chat_completion"), json=json_body) as response:
#             response_data = await response.json()
#             answer = response_data["answer"]
#             history = response_data["history"]

#     async with get_sessionmaker().begin() as db_session:
#         db_session: AsyncSession
#         await db_session.execute(
#             update(UserSettings)
#             .where(UserSettings.user_fk == message.from_user.id)
#             .values(history=history)
#         )
#     return answer
