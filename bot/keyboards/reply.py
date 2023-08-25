from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, WebAppData
from aiogram.utils.web_app import safe_parse_webapp_init_data
from os import getenv


class ReplyKeyboards:

    __URL = getenv("BABYFALCON_URL")

    @classmethod
    def main(cls, user_id: int) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardBuilder()
        kb.add(
            KeyboardButton(text="Промпт"),
            # KeyboardButton(
            #     text="История",
            #     web_app=WebAppInfo(
            #         url=f"{cls.__URL}/pages/history-menu/{user_id}")
            # ),
            # KeyboardButton(
            #     text="Креативность",
            #     web_app=WebAppInfo(
            #         url=f"{cls.__URL}/pages/creativity/{user_id}",
            #     )),
        )
        kb.row(
            KeyboardButton(text="Добавить документ")
        )
        kb.row(
            KeyboardButton(text="Информация"), KeyboardButton(text="Задачи")
        )
        return kb.as_markup(resize_keyboard=True)

    @staticmethod
    def button(text: str) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardBuilder()
        kb.row(
            KeyboardButton(text=text)
        )
        return kb.as_markup(resize_keyboard=True)
