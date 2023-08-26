from aiogram.types import Message, CallbackQuery, ContentType
from aiogram import F
from aiogram import Dispatcher
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode


from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


# from llm.llm import ask_chain
from ..keyboards import RK, IK
# update_prompt, erase_history,
from bot.services.gptapi import chat_completion
from bot.services.db import get_user_data, update_user_data, update_model_documents, get_drive_folder_id
from bot.services.db import models as M


# ADMIN_IDS = ["638322484"]
# GROUP_ID = "@FrisbiChat"


async def get_start(message: Message) -> None:
    await message.answer(
        """"Добро пожаловать!

Я - виртуальный менеджер детского центра IQ Baby Palace.
Я создан на основе большой языковой модели GPT4, поэтому смогу ответить на любые вопросы (по нашему клубу), заданные в свободной форме!
В этом боте вы сможете отслеживать ваши занятия, записываться на мастер-классы и получать консультации 24/7."

Наверное этот текст будут видеть пользователи бота. Чё думаете?
""",
        reply_markup=RK.main(message.from_user.id))


class PromptReset(StatesGroup):
    s1 = State()


class DocsLoad(StatesGroup):
    s1 = State()


async def get_prompt(message: Message):
    user = await get_user_data(M.OUser(id=message.from_user.id))
    await message.answer(
        f'<b>Текущий промпт:</b>\n\n"""\n<i>{user.settings.prompt}</i>\n"""',
        parse_mode=ParseMode.HTML,
        reply_markup=IK.button("Обновить промпт♻️",
                               callback_data="RESET_PROMPT")
    )


async def reset_prompt(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        'Введите новый промпт:',
        reply_markup=RK.button("Отмена")
    )
    await state.set_state(PromptReset.s1)


async def get_new_prompt(message: Message, state: FSMContext):

    await update_user_data(M.OUser(id=message.from_user.id, settings=M.OSettings(prompt=message.text)))
    await message.answer("Промт был обновлен!", reply_markup=RK.main(message.from_user.id))
    await state.clear()


async def update_documents(message: Message, state: FSMContext):
    await message.answer("Пришлите текст для сохранения")
    await state.set_state(DocsLoad.s1)


async def get_documents(message: Message, state: FSMContext):
    result = await update_model_documents(message.from_user.id, message.from_user.username, message.text)
    await message.answer(result)
    await state.clear()


async def get_temperature(message: Message):
    await update_user_data(
        M.OUser(
            id=message.from_user.id,
            settings=M.OSettings(model_temperature=float(message.web_app_data.data) / 100.))
    )
    await message.answer(f"Настройки креативности изменены!\n\n\
Новый уровень креативности - <b>{message.web_app_data.data}%</b>", parse_mode=ParseMode.HTML)


async def get_info(message: Message) -> None:
    folder_id = await get_drive_folder_id(message.from_user.id)
    await message.answer(
        """Продублирую наши цели на свякий.

Необходимо "натренировать" ассистента так, чтобы он:
1. Был вежлив
2. Правильно отвечал на любой вопрос по IQBabyPalace
3. Отвечал на вопросы по воспитанию детей и все в этом духе
4. НЕ отвечал на вопросы не связанные с этим ( скорее отвечал, что это вопрос не по теме)
5. НЕНАВЯЗЧИВО предлагал наши услуги, если это позволяет контекст
6. Не придумывал отсебятину, путающую клиентов
        
Ссылки на полезную инфу:
- <a href="https://www.pinecone.io/learn/what-is-similarity-search/">Эмбеддинги.</a>
- <a href="https://ya.zerocoder.ru/kak-pisat-effektivnye-promty-dlya-nejroseti/">Основы промпт енджинеринга.</a>
- <a href="https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api">Формирования промпта.</a>
---новые---
- <a href="https://habr.com/ru/articles/731056/">Про реализацию.</a>
-----------
Некоторые ресурсы на английском, но они простые, поэтому либо вы всё поймёте либо переводчик браузера всё переведёт достаточно чётко.

Если будет что то непонятно, повторюсь, пишите мне. Но так же можете спросить у бота. Он поумнее будет)
""", parse_mode=ParseMode.HTML, reply_markup=IK.info(folder_id))


async def cancel_state(message: Message, state: FSMContext):
    await message.answer("Действие отменено.", reply_markup=RK.main(message.from_user.id))
    await state.clear()


async def any_message(message: Message) -> None:
    answer = await chat_completion(message.from_user.id, message.text)
    await message.answer(answer)


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(get_start, Command(commands=["start"]))
    dp.message.register(cancel_state, F.text == "Отмена")
    dp.message.register(get_prompt,  F.text == "Промпт")
    dp.callback_query.register(reset_prompt, F.data == "RESET_PROMPT")
    dp.message.register(get_new_prompt,  PromptReset.s1)
    dp.message.register(update_documents, F.text == "Добавить документ")
    dp.message.register(get_documents, DocsLoad.s1)
    dp.message.register(get_temperature,  F.content_type.in_(
        ContentType.WEB_APP_DATA,))
    dp.message.register(get_info,  F.text == "Информация")
    dp.message.register(any_message)
