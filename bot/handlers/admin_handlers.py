from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram import Dispatcher
from aiogram.filters.command import Command

# from llm.llm import ask_chain
from ..keyboards import RK


def register_handlers(dp: Dispatcher) -> None:
    # dp.message.register(get_start_for_admin, Command(commands=["start"]))
    ...
