from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message
from pprint import pp

router = Router()


class Authenticated(Filter):

    async def __call__(self, message: Message, authenticated: bool) -> bool:
        return authenticated == True
