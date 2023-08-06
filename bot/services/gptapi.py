import aiohttp
from aiogram.types import Message
from db import get_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam
from sqlalchemy.orm import sessionmaker as _sessionmaker
from pydantic import BaseModel


from db.models import User, UserSettings


class API:
    API_URL = "http://localhost:8000"

    API_ENDPOINTS = {
        "home": "/",
        "init_admin": "/bot/init-admin/",
        "chat_completion": "/bot/chat-compeltion",
    }

    @classmethod
    def get_url(cls, endpoint_name: str):
        return cls.API_URL + cls.API_ENDPOINTS.get(endpoint_name)


async def init_admin(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(API.get_url("init_admin"), json={"username": username}) as response:
            print(await response.json())

BASE_PROMPT_TEMPLATE = """

Ниже, предоставлен справочный материал по данному вопросу. Вы можете руководствоваться им, для повышения точности ответа.

Начало справочного материала.
[{}]
Конец справочного материала.
"""


async def chat_completion(message: Message) -> str:

    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        res = await db_session.execute(select(UserSettings).where(
            UserSettings.user_fk == message.from_user.id))

        settings = res.scalar_one_or_none()

        if not settings:
            raise Exception()

        json_body = {
            "name": settings.user.first_name,
            "query": message.text,
            "model_temperature": settings.model_temperature,
            "prompt": settings.prompt,
            "history": settings.history,
        }

    print(json_body)
    async with aiohttp.ClientSession() as session:
        async with session.post(API.get_url("chat_completion"), json=json_body) as response:
            response_data = await response.json()
            answer = response_data["answer"]
            history = response_data["history"]

    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        await db_session.execute(
            update(UserSettings)
            .where(UserSettings.user_fk == message.from_user.id)
            .values(history=history)
        )
    return answer
