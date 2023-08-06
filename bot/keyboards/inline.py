from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboards:

    @staticmethod
    def button(text: str, url: str = None, callback_data: str = None, **kwargs) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=text, url=url,
                                 callback_data=callback_data,  **kwargs)
        )
        return kb.as_markup()
