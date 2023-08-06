from aiogram import Dispatcher

from .register_user import Register


def register_middlewares(dp: Dispatcher) -> None:
    dp.message.outer_middleware(Register())
