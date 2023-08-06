import aiohttp
from aiogram.types import Message
from db import get_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete
from sqlalchemy.orm import sessionmaker as _sessionmaker


from db.models import User, UserSettings


async def get_user_data(user_id: int) -> User:
    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        res = await db_session.execute(
            select(User)
            .where(User.id == user_id)
        )

        user = res.scalar_one_or_none()
        if not user:
            raise Exception("User was not found.")

        db_session.expunge_all()
        return user


async def update_prompt(user_id: int, new_prompt: str) -> None:
    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        await db_session.execute(
            update(UserSettings)
            .where(UserSettings.user_fk == user_id)
            .values(prompt=new_prompt)
        )


async def erase_history(user_id: int) -> None:
    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        await db_session.execute(
            update(UserSettings)
            .where(UserSettings.user_fk == user_id)
            .values(history=[])
        )
