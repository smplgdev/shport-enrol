import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from db.base import get_session
from db.commands import create_tables
from handlers import add_tracking_link
from handlers.commands import start
from services.setup_logging import setup_logging

load_dotenv()

setup_logging()

logger = logging.getLogger(__name__)

TG_BOT_API_TOKEN = os.getenv("TG_BOT_API_TOKEN")

bot = Bot(TG_BOT_API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))


async def main():
    session = get_session(os.getenv("DB_PATH"))
    create_tables(session)

    dp = Dispatcher(session=session)

    dp.include_router(start.router)
    dp.include_router(add_tracking_link.router)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()

if __name__ == "__main__":
    asyncio.run(main())
