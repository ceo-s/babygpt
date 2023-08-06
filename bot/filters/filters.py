from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message
from pprint import pp

router = Router()


class Authorized(Filter):

    async def __call__(self, message: Message, authorized: bool) -> bool:
        return authorized == True
