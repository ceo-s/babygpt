from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Dispatcher
from aiogram.filters.command import Command

# from llm.llm import ask_chain
from ..keyboards import RK
from ..filters import Authorized


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
        'Всем привет!\n\n\
В этом боте вы сможете проводить тестирование промптов и базы документов для ассистента на базе GPT-3.5.\n\n\
Нам необходимо его "натренировать" так, чтобы он:\n\
1. Был вежлив\n\
2. Правильно отвечал на любой вопрос по BabyPalace\n\
3. Отвечал на вопросы по воспитанию детей и все в этом духе\n\
4. НЕ отвечал на вопросы не связанные с этим ( скорее отвечал, что это вопрос не по теме)\n\
5. НЕНАВЯЗЧИВО предлагал наши услуги, если это позволяет контекст\n\
6. Не придумывала отсебятину, путающую клиентов. (Да так бывает)\n\n\
Нажмите на кнопку, когда будете готовы начать обучение. Удачи!\n\
', reply_markup=RK.button("Начать"))

    await state.set_state(Tutorial.s1)


async def get_s1(message: Message, state: FSMContext):
    await message.answer(
        'Мы хотим сделать ассистента (виртуального помощника/чат бота), который мог бы непринужденно общаться \
с клиентами и отвечал на любые вопросы 24/7.\n\n\
Дальше будет небольшой ликбез и пара рекомендаций.\n\n\
Сразу скажу, если понятно все - красава.\n\
Если теория не понятна, а что делать понятно - можете приступать, всё норм.\n\
Если ниче не понятно или возникнут вопросы в процессе - пишем <a href="t.me/ceo_of_seks">мне</a>.\
', reply_markup=RK.button("Понял, дальше."), parse_mode=ParseMode.HTML)
    await state.set_state(Tutorial.s2)


async def get_s2(message: Message, state: FSMContext):
    await message.answer(
        'Что вообще такое GPT?\n\n\
Она и ей подобные программы называются большими языковыми моделями. \
Их внутреннее устройство сложное, но идея проста. Они предсказывают следующее слово, исходя из всех предыдущих. \
Прямо как наш мозг.\n\
По сути она читает что мы ей напишем и слово за словом генерирует ответ. \
Но... как? \n\n\
Она "обучена" на большом количестве текста из интернета. \
И для нас не важно что под капотом и что вообще значит "обучать" программу. \
Для нас важно то что она круто работает с текстом на любом языке и шарит почти во всем.\
', reply_markup=RK.button("Круто, дальше."))
    await state.set_state(Tutorial.s3)


async def get_s3(message: Message, state: FSMContext):
    await message.answer(
        'Ага, ещё круче, что она не имеет ни характера, ни желаний, ни мнения, \
а значит полностью под нашим контролем. \n\n\
Мы можем ее направлять, указывать как себя вести: всегда или в определённых ситуациях. \
Необходимо дать ей такой набор инструкций, чтобы её поведение соответствовало нашим ожиданиям.\n\n\
Такой набор инструкций правильно называется - prompt(промпт).\n\n\
На <a href="https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api">этом сайте</a> \
вы можете ознакомиться с рекомендациями по составлению промптов.\n\n\
После обучения у вас появится кнопка "Промпт".\n\n\
Кстати, как закончим, сможете добавить в резюме новый модный навык - promp engineering.\
', parse_mode=ParseMode.HTML, reply_markup=RK.button("Promp engineering? Я мечтал об этом!"))
    await state.set_state(Tutorial.s4)


async def get_s4(message: Message, state: FSMContext):
    await message.answer(
        'Ещё у модели можно настраивать уровень креативности. \
Чем он выше, тем более разнообразные ответы модель будет выдавать. \
Но это может приводить к непредсказуемым результатам и потере точности.\n\
Необходимо найти золотую середину.\n\n\
После обучения у вас появится кнопка "Креативность".\
',  reply_markup=RK.button("Удобно! Не придётся писать в промпте насколько веселой ей быть. Дальше."))
    await state.set_state(Tutorial.s5)


async def get_s5(message: Message, state: FSMContext):
    await message.answer(
        'Да, а ещё не придётся заботиться о том чтобы она помнила о чем вы говорили. \
Она может помнить n-ное количество сообщений из вашего диалога, так как сохраняет их в историю. \
Вы сможете регулировать это количесвто сообщений самостоятельно. Зачем? Очевидно, что помнить 1000 сообщений \
куда тяжелее чем 10. Поэтому тут мы размениваем точность на память. \
Так же вы сможете очищать историю диалога, чтобы, например, после смены промпта, модель не путали её же старые ответы \
из истории диалога.\
После обучения появится кнопка "История".\
',  reply_markup=RK.button("Окей, давай дальше."))
    await state.set_state(Tutorial.s6)


async def get_s6(message: Message, state: FSMContext):
    await message.answer(
        'Ладно, с поведением разобрались. Но что с информацией по клубу?\n\n\
Очевидно разработчики не обучали ее на подобных данных. \
Об этом предстоит позаботиться уже нам. \
Мы должны подготовить для модели перечень документов, содержащих информацию о нашем клубе.\n\n\
Абсолютно всю информацию, которую мы хотим, чтобы ассистент знал:\n\
-Цены\n\
-Расписание (чтобы любой маньяк был в курсе когда детишки заканчивают)\n\
-Подробное описание занятий \n\
-Ваши биографии (профессиональные качества и заслуги, чтоб знали что у нас ток профи)\n\
-Сценарии общения с клиентом (выдуманные диалоги с эталонными ответами на распространённые вопросы, FAQ)\n\
-Если есть идеи добавляем ещё что нибудь\n\n\
Так просто??? Ну как бы да... но нет.\n\
На качество работы будет очень сильно влиять формат этих самых документов. \
Задача не просто впихнуть туда все что можно, а структурировать информацию так, \
чтобы модель их качественно обработала и поняла смысл.\n\n\
Как это делать вы возможно узнаете дальше, а пока что посмотрите что будет если этого НЕ ДЕЛАТЬ. \
*Видео*\
', reply_markup=RK.button("Да, я точно посмотрел это видео, дальше."))
    await state.set_state(Tutorial.s7)


async def get_s7(message: Message, state: FSMContext):
    await message.answer(
        'Верю. Как GPT вообще работает с этими документами?\n\n\
Она их не запоминает все разом. \nМы её не "дообучаем", а просто даем ей дополнительную информацию, \
которая может помочь ответить на конкретный вопрос. \n\n\
Она как бы выборочно читает что то из списка документов перед каждым вопросом, пытаясь найти там ответ.\n\n\
Например у нас есть 2 документа. Первый - цены. Второй - расписание.\
Если клиент задаст вопрос по расписанию, модель прочитает только второй документ. И наоборот. \
Этого будет достаточно, чтобы ответить на вопрос.\n\
', reply_markup=RK.button("Это то понятно, а что там с форматом то?"))
    await state.set_state(Tutorial.s8)


async def get_s8(message: Message, state: FSMContext):
    await message.answer(
        'Тут однозначного ответа как делать надо и не надо я всё таки дать не могу.\n\n\
Вам надо будет поэкспериментировать с:\n\
- Размером документов.\n\
- Прямолинейностью изложения (?) ну тип сухо или в деталях. Тезисно или в свободном формате.\n\
- Перефразированием одних и тех же вещей в рамке одного документа.\n\n\
Короче много всего.\nНаверное большинство проблем, были показаны в видео. Например она не понимала о каком раписании идет речь \
или придумывала новые секции типо плавания. И вообще так себе с ней было общаться.\
В общем надо будет немного покреативить.\
', reply_markup=RK.button("Нихера не понятно... А загружать документы куда?"))
    await state.set_state(Tutorial.s9)


async def get_s9(message: Message, state: FSMContext):
    await message.answer(
        'Все документы надо будет загружать на \
<a href="https://drive.google.com/drive/u/1/folders/1f7o4aD60tka0ehhv4WuSaeQ-2Uy-mAN0">этот гугл диск</a> \
в вашу папку. Она уже создана и названа никнеймом из телеграма (переименовывать нельзя!). \n\
Текста, с которыми работала модель в видео находятся в папке "Видео", там все данные скопированны с сайта. \
', parse_mode=ParseMode.HTML, reply_markup=RK.button("Ну окей. А саму информацию из головы чтоли брать?"))
    await state.set_state(Tutorial.s10)


async def get_s10(message: Message, state: FSMContext):
    await message.answer(
        'Нет, в папке "Общая" на диске лежат файлы со всей информацией по IQ Baby Palace.\n\
Cкопируйте всё в свою папку, а затем начинайте редактировать. \
Так же добавлять что то полезное от себя не запрещается. Можете добавить статьи по воспитанию и тд. я хз крч.\
', reply_markup=RK.button("А подходят только текстовые файлы?"))
    await state.set_state(Tutorial.s11)


async def get_s11(message: Message, state: FSMContext):
    await message.answer(
        'Нет, можете добавлять вордовские файлы с расширением <b>.docx</b> , обычные текстовые <b>.txt</b> файлы и \
файлы екселя <b>.xlsx</b> .\nТабличные данные будут сами переводиться в текст практически без изменений.\n\
Думаю это удобно например для цен и расписания.\
', parse_mode=ParseMode.HTML, reply_markup=RK.button("Ну ладно. Лучше тебя никто бы не объснил, спасибо!"))
    await state.set_state(Tutorial.s12)


async def get_s12(message: Message, state: FSMContext):
    await message.answer('Не за что.\nНа этом всё, творите! Желаю удачи!', reply_markup=RK.main)
    await state.clear()


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(get_start_for_admin, Command(
        commands=["start"]), ~Authorized())
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
