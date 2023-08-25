from aiogram.types import Message, CallbackQuery, ContentType
from aiogram import F
from aiogram import Dispatcher
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode
from sqlalchemy.orm import sessionmaker as _sessionmaker


from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


# from llm.llm import ask_chain
from ..keyboards import RK, IK
# update_prompt, erase_history,
from bot.services.gptapi import chat_completion
from bot.services.db import get_user_data, update_user_data, update_model_documents
from bot.services.db import models as M


# ADMIN_IDS = ["638322484"]
# GROUP_ID = "@FrisbiChat"


async def get_start(message: Message) -> None:
    await message.answer(
        """
Добро пожаловать!

Я - виртуальный менеджер детского центра IQ Baby Palace.
Я создан на основе большой языковой модели GPT4, поэтому смогу ответить на любые вопросы (по нашему клубу), заданные в свободной форме!
В этом боте вы сможете отслеживать ваши занятия, записываться на мастер-классы и получать консультации 24/7.""",
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

# async def get_history(message: Message):
#     user = await get_user_data(message.from_user.id)
#     await message.answer(user.first_name)


# async def reset_history(message: Message):
#     try:
#         await erase_history(message.from_user.id)
#         await message.answer("История очищена!")
#     except Exception as ex:
#         await message.answer(ex)


async def get_temperature(message: Message):
    await update_user_data(
        M.OUser(
            id=message.from_user.id,
            settings=M.OSettings(model_temperature=float(message.web_app_data.data) / 100.))
    )
    await message.answer(f"Настройки креативности изменены!\n\n\
Новый уровень креативности - <b>{message.web_app_data.data}%</b>", parse_mode=ParseMode.HTML)


async def get_info(message: Message) -> None:
    user = await get_user_data(M.OUser(id=message.from_user.id))
    await message.answer(
        'Здесь всякая инфа. \n\
', parse_mode=ParseMode.HTML, reply_markup=IK.info(user.collection.dir_id))


# async def get_tasks(message: Message) -> None:
#     await message.answer(
#         'Нам необходимо его "натренировать" так, чтобы он:\n\
# 1. Был вежлив\n\
# 2. Правильно отвечал на любой вопрос по BabyPalace\n\
# 3. Отвечал на вопросы по воспитанию детей и все в этом духе\n\
# 4. НЕ отвечал на вопросы не связанные с этим ( скорее отвечал, что это вопрос не по теме)\n\
# 5. НЕНАВЯЗЧИВО предлагал наши услуги, если это позволяет контекст\n\
# 6. Не придумывала отсебятину, путающую клиентов. (Да так бывает)\n\n\
# ')


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
#     dp.message.register(get_history,  F.text == "История")
    dp.message.register(get_temperature,  F.content_type.in_(
        ContentType.WEB_APP_DATA,))
    dp.message.register(get_info,  F.text == "Информация")
#     dp.message.register(get_tasks, F.text == "Задачи")
    # dp.message.register(any_message)
