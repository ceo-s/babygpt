from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, WebAppData
from aiogram.utils.web_app import safe_parse_webapp_init_data


class ReplyKeyboards:

    @property
    def main(self) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardBuilder()
        kb.add(
            KeyboardButton(text="Промпт"),
            KeyboardButton(
                text="История",
                web_app=WebAppInfo(
                    url="https://5c29-188-243-182-231.ngrok-free.app/bot/history/")
            ),
            KeyboardButton(
                text="Креативность",
                web_app=WebAppInfo(
                    url=f"https://5c29-188-243-182-231.ngrok-free.app/bot/creativity/?temperature=1",
                )),
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
