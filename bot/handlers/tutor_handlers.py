from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Dispatcher
from aiogram.filters.command import Command
from bot.services.db import get_drive_folder_id

# from llm.llm import ask_chain
from ..keyboards import RK
from ..filters import Authenticated


class Tutorial(StatesGroup):
    s1 = State()
    s2 = State()
    s3 = State()
    s4 = State()
    s5 = State()
    s6 = State()
    s7 = State()
    s8 = State()
    s9 = State()
    s10 = State()
    s11 = State()
    s12 = State()


async def get_start_for_admin(message: Message, state: FSMContext):
    await message.answer(
        """Всем привет!
Тезисно обозначу задачи.
Нам необходимо "натренировать" ассистента так, чтобы он:
1. Был вежлив
2. Правильно отвечал на любой вопрос по IQBabyPalace
3. Отвечал на вопросы по воспитанию детей и все в этом духе
4. НЕ отвечал на вопросы не связанные с этим (скорее отвечал, что это вопрос не по теме)
5. НЕНАВЯЗЧИВО предлагал наши услуги, если это позволяет контекст
6. Не придумывал отсебятину, путающую клиентов (да так бывает)
Нажмите на кнопку, когда будете готовы начать обучение. Удачи!
""", reply_markup=RK.button("Начать"))

    await state.set_state(Tutorial.s1)


async def get_s1(message: Message, state: FSMContext):
    await message.answer(
        """Мы хотим сделать ассистента (виртуального помощника/чат бота), который мог бы непринужденно общаться с клиентами и отвечал на любые вопросы 24/7.

Дальше будет небольшой ликбез и пара рекомендаций.
Сразу скажу, если всё понятно - красава.
Если теория не понятна, а что и как делать - понятно, то можете приступать, всё норм.
Если возникнут вопросы - пишем <a href="t.me/ceo_of_seks">мне</a>.
""", reply_markup=RK.button("Понял, дальше."), parse_mode=ParseMode.HTML)
    await state.set_state(Tutorial.s2)


async def get_s2(message: Message, state: FSMContext):
    await message.answer(
        """Что вообще такое GPT?

Она и ей подобные программы называются большими языковыми моделями.

Их внутреннее устройство сложное, но идея проста. Они предсказывают следующее слово, исходя из всех предыдущих.
Прямо как наш мозг.

Такая программа получает какой то текст (и только), читает, и слово за словом генерирует ответ, а потом возвращает его.

- Но как?
- Ааа... Эээ... Нууу... Всё сложно крч.

В кратце - она "обучена" на большом количестве текста из интернета.
И для нас не особо важно что вообще значит "обучать" программу в данном контексте.
Важно только то, что она очень хорошо этот текст помнит, так что это превращает её в ходячую (ну тип) энциклопедию.


Это тоже самое что и Chat GPT?

Немного другое. По факту - обычный чат!
Прослойка между пользователем и большой языковой моделью, предоставляющая удобный интерфейс.
""", reply_markup=RK.button("Ниче нового, дальше!"))
    await state.set_state(Tutorial.s3)


async def get_s3(message: Message, state: FSMContext):
    await message.answer(
        """GPT на самом деле уже довольно зацензурена (так было не всегда), поэтому сильно переживать за вежливость нам не нужно.
Разработчики её надрессировали быть "Полезным виртуальным помощником".

В любом случае, мы можем ее направлять, указывать как себя вести: всегда или в определённых ситуациях.
Необходимо дать ей такой набор инструкций, чтобы её поведение соответствовало нашим ожиданиям. (Например нам важно, чтобы наш ассистент не говорил на темы отличные от детского развития и тд.)

Такой набор инструкций правильно называется - prompt (промпт).

На <a href="https://ya.zerocoder.ru/kak-pisat-effektivnye-promty-dlya-nejroseti/">этом сайте</a> вы можете ознакомиться с рекомендациями по составлению промптов.

После обучения у вас появится кнопка "Промпт".
P.S. Кстати, как закончим, сможете добавить в резюме новый модный навык - prompt engineering.
""", parse_mode=ParseMode.HTML, reply_markup=RK.button("Prompt engineering? Я мечтал об этом!"), disable_web_page_preview=True)
    await state.set_state(Tutorial.s4)


async def get_s4(message: Message, state: FSMContext):
    await message.answer(
        """Ещё у модели можно настраивать уровень креативности. Чем он выше, тем более разнообразные ответы модель будет выдавать. Но это может приводить к непредсказуемым результатам и потере точности.
Необходимо найти золотую середину (это не обязательно будет 50%😃).

После обучения у вас появится кнопка "Креативность".
""",  reply_markup=RK.button("Удобно! Не придётся это прописывать в промпте. Дальше!"))
    await state.set_state(Tutorial.s5)


async def get_s5(message: Message, state: FSMContext):
    await message.answer(
        """Если вы внимательно слушали, то помните что большие языковые модели просто принимают текст и возвращают ответ.
Больше они ничего не имеют. Но если вспомнить опыт общения с Chat GPT, то <a href="https://www.youtube.com/watch?v=5GfDNLz_-yU">встает вопрос</a>, а как они тогда помнят историю диалога???

Вот это как раз одна из плюшек именно чата. Текст прошлых сообщений отправляется вместе с новым запросом. Всё логично.
У нас есть возможность регулировать количество сообщений, сохраняемых в историю.

Зачем? Очевидно, что помнить 1000 сообщений куда тяжелее чем, например 4. Поэтому тут мы размениваем точность на память.

Так же вы сможете очищать историю диалога, чтобы, например, после смены промпта, модель не путали её же старые ответы из истории диалога.

После обучения у вас появится кнопка "История".
""", parse_mode=ParseMode.HTML, reply_markup=RK.button("Окей, давай дальше."), disable_web_page_preview=True)
    await state.set_state(Tutorial.s6)


async def get_s6(message: Message, state: FSMContext):
    await message.answer(
        """Ладно, с поведением разобрались. Но что с информацией по клубу?

Очевидно разработчики не обучали ее на подобных данных. 
Об этом предстоит позаботиться уже нам. 
Мы должны подготовить для модели перечень документов, содержащих информацию о нашем клубе.

Абсолютно всю информацию, которую мы хотим, чтобы ассистент знал:
-Цены
-Расписание (чтобы любой маньяк был в курсе когда детишки заканчивают)
-Подробное описание занятий 
-Ваши биографии (профессиональные качества и заслуги, чтоб знали что у нас ток профи)
-Сценарии общения с клиентом (выдуманные диалоги с эталонными ответами на распространённые вопросы, FAQ)
-Если есть идеи добавляем ещё что нибудь

Так просто??? Ну как бы да... но нет.

На качество работы будет очень сильно влиять формат этих самых документов. Задача не просто впихнуть туда все что можно, а структурировать информацию так, чтобы модель их качественно обработала и поняла смысл.
""", reply_markup=RK.button("Э, а как???."))
    await state.set_state(Tutorial.s7)


async def get_s7(message: Message, state: FSMContext):
    await message.answer(
        """Тут однозначного ответа как делать надо и не надо я всё таки дать не могу.
Всё узнаем в процессе. Надо будет поэкспериментировать.

Вот что я думаю нужно проверить:
- Лучше описывать официально или в том стиле, в котором ассистенту стоит отвечать?
- Лучше писать красноречиво или тезисно?
- Стоит ли повторяться в документах, перефразируя одни и те же фразы?

Короче я хз чё ещё. По сути думать тут много не надо. Эмпирически найдёте оптимаьный формат)
""", reply_markup=RK.button("А эти документы мы как передаем GPT?"))
    await state.set_state(Tutorial.s8)


async def get_s8(message: Message, state: FSMContext):
    await message.answer(
        """Хороший вопрос. Так - же. Как и историю и сам новый запрос, отправляем текстом. И, нет, не все сразу.

Например, у нас есть 2 документа:
- цены
- расписание

Если клиент задаст вопрос по расписанию, модель "прочитает" только второй документ. И наоборот.

Вообще, если совсем честно, это поведение не обязательно и обоснованно только ограничениями вычислительных мощностей тарифа и здравым смыслом.

Когда я говорю, что модель "читает" что-то, я на самом деле имею ввиду, что мы по определённому алгоритму выбираем, какой документ вероятнее всего содержит ответ на вопрос и отправляем его содержимое вместе с самим вопросом.

Для самых любознательных - этот алгоритм основан на поиске ближайших соседей в пространстве <a href="https://www.pinecone.io/learn/what-is-similarity-search/">эмбеддингов</a>.
""", parse_mode=ParseMode.HTML, reply_markup=RK.button("Окей, а загружать документы куда?"), disable_web_page_preview=True)
    await state.set_state(Tutorial.s9)


async def get_s9(message: Message, state: FSMContext):
    folder_id = await get_drive_folder_id(message.from_user.id)
    link = f"https://drive.google.com/drive/folders/{folder_id}?usp=drive_link"
    await message.answer(
        """
Да вот сюда вот - <a href="{link}">ваша папка на гугл диске</a>.
Открываете на компе, и перетаскиваете туда все нужные файлы.
""".format(link=link), parse_mode=ParseMode.HTML, reply_markup=RK.button("А подходят только текстовые файлы?"))
    await state.set_state(Tutorial.s10)


async def get_s10(message: Message, state: FSMContext):
    await message.answer(
        """Нет, можете добавлять вордовские файлы с расширением <b>.docx</b>, файлы формата гугл документ (как вордовский, но прям в гугл диске), обычные текстовые <b>.txt</b> файлы и файлы екселя <b>.xlsx</b> (ну или гугл таблицы).

Табличные данные я перевожу в формат как на фото. То есть пока не очень разнообразно, но можно накидать FAQ.
А может и не пока, может только так и оставлю. Сложность в том, что мне не определить как мне парсить файлы при загрузке с гугл диска, без дополнительных указаний с вашей стороны. А это надо уже обсуждать... Если есть идеи отпишите мне)
""", parse_mode=ParseMode.HTML, reply_markup=RK.button("А инфу откуда брать кста?"))
    await state.set_state(Tutorial.s11)


async def get_s11(message: Message, state: FSMContext):
    await message.answer(
        "У Сергея Евгеньевича!", reply_markup=RK.button("ОК!"))
    await state.set_state(Tutorial.s12)


async def get_s12(message: Message, state: FSMContext):
    await message.answer(
        """На этом всё.
Надеюсь ничего не забыл. Чтобы вы тоже ничего не забыли, добавил кнопку "Информация".

Удачи!""", reply_markup=RK.main(message.from_user.id))
    await state.clear()


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(get_start_for_admin, Command(
        commands=["start"]), ~Authenticated())
    dp.message.register(get_s1, Tutorial.s1)
    dp.message.register(get_s2, Tutorial.s2)
    dp.message.register(get_s3, Tutorial.s3)
    dp.message.register(get_s4, Tutorial.s4)
    dp.message.register(get_s5, Tutorial.s5)
    dp.message.register(get_s6, Tutorial.s6)
    dp.message.register(get_s7, Tutorial.s7)
    dp.message.register(get_s8, Tutorial.s8)
    dp.message.register(get_s9, Tutorial.s9)
    dp.message.register(get_s10, Tutorial.s10)
    dp.message.register(get_s11, Tutorial.s11)
    dp.message.register(get_s12, Tutorial.s12)
