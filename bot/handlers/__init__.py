from importlib import import_module
from aiogram import Dispatcher
from .base_handlers import register_handlers

HANDLERS_MODULES = [
    "tutor_handlers",
    "base_handlers",
    "admin_handlers",
]


def register_handlers(dp: Dispatcher) -> None:
    for module_name in HANDLERS_MODULES:
        module = import_module("." + module_name, "bot.handlers")
        module.register_handlers(dp=dp)
