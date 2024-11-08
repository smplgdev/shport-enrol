from aiogram import Router, F
from aiogram.types import Message

from db.commands import add_event
from db.utils import DatabaseSession
from services.api import fetch_page_title

router = Router()


@router.message(F.text.regexp(r'https://sportup\.si/dogodki/*'))
async def link_handler(message: Message, session: DatabaseSession) -> None:
    try:
        event_name = fetch_page_title(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    add_event(session, event_name, message.text)
    await message.answer(f"Added event {event_name}")


@router.message()
async def other_messages_handler(message: Message) -> None:
    await message.answer("Hey! Send me the correct link to the Šport UP event and I'll notify you when booking is available!")
