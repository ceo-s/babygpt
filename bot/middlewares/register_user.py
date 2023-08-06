from typing import Awaitable, Callable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker as _sessionmaker
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from pprint import pp

from db.models import User, UserSettings
from ..services.gptapi import init_admin


class Register(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        sessionmaker: _sessionmaker = data.get("sessionmaker")

        async with sessionmaker.begin() as session:
            session: AsyncSession

            res = await session.execute(select(User).where(User.id == event.from_user.id))
            user = res.one_or_none()

            if user:
                data["authorized"] = True
                print("User authorized")
            else:
                user = User(
                    id=event.from_user.id,
                    username=event.from_user.username,
                    first_name=event.from_user.first_name
                )

                # history = [{
                #     "role": "user",
                #     "content": event.text,
                #     "name": event.from_user.first_name,
                # }]

                user_settings = UserSettings(
                    model_temperature=0.5,
                    prompt="Ты - полезный чат-бот.",
                    history=[],
                )

                user.settings = user_settings
                await session.merge(user)
                await init_admin(event.from_user.username)
                data["authorized"] = False
                print("User is not authorized")

        return await handler(event, data)
