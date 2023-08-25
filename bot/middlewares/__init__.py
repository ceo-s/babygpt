from aiogram import Dispatcher

from .authenticate_user import Authenticate


def register_middlewares(dp: Dispatcher) -> None:
    dp.message.outer_middleware(Authenticate())
