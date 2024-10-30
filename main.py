import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from handlers import echo
from handlers.commands import start
from services.setup_logging import setup_logging


logger = logging.getLogger(__name__)

load_dotenv()
TG_BOT_API_TOKEN = os.getenv("TG_BOT_API_TOKEN")


async def main():
    setup_logging()

    bot = Bot(TG_BOT_API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(echo.router)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()

if __name__ == "__main__":
    asyncio.run(main())
