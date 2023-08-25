from dotenv import load_dotenv
import asyncio

from bot import DISPATCHER, BOT
from bot.handlers import register_handlers
from bot.middlewares import register_middlewares

load_dotenv(".env")


def setup():
    register_middlewares(DISPATCHER)
    register_handlers(DISPATCHER)


async def main():
    await DISPATCHER.start_polling(BOT)


if __name__ == "__main__":
    setup()
    asyncio.run(main())
