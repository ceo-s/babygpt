from dotenv import load_dotenv
import asyncio

from bot import DISPATCHER, BOT
from bot.handlers import register_handlers
from bot.middlewares import register_middlewares
from db import get_sessionmaker

load_dotenv(".env")


def setup():
    register_middlewares(DISPATCHER)
    register_handlers(DISPATCHER)


async def main():
    sessionmaker = get_sessionmaker()
    await DISPATCHER.start_polling(BOT, sessionmaker=sessionmaker)


if __name__ == "__main__":
    setup()
    asyncio.run(main())
