from typing import Awaitable, Callable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker as _sessionmaker
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from pprint import pp

from ..services.db import models as M, authenticate_user


class Authenticate(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_in_database = await authenticate_user(M.User(
            id=event.from_user.id,
            username=event.from_user.username,
            first_name=event.from_user.first_name,
        ))

        if user_in_database:
            data["authenticated"] = True
        else:
            data["authenticated"] = False

        return await handler(event, data)