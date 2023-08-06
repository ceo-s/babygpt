import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv(".env")

bot = Bot(os.getenv("BABY_PALACE"))
dp = Dispatcher()
