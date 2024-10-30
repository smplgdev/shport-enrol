from aiogram import Router
from aiogram.types import Message

from services.tracking import start_tracking
from services.api import check_link

router = Router()


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        if check_link(message.text):
            await start_tracking(message)
        else:
            await message.answer("Invalid link")
    except TypeError:
        await message.answer("Unsupported message type")
