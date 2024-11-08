from aiogram import Router
from aiogram.types import Message

from db.commands import add_event
from db.utils import DatabaseSession
from services.api import is_link, fetch_page_title

router = Router()


@router.message()  # TODO: add magic filter for links
async def echo_handler(message: Message, session: DatabaseSession) -> None:
    try:
        if is_link(message.text):
            try:
                event_name = fetch_page_title(message.text)
            except ValueError as e:
                await message.answer(str(e))
                return

            add_event(session, event_name, message.text)
            await message.answer(f"Added event {event_name}")
        else:
            await message.answer("Invalid link")
    except TypeError:
        await message.answer("Unsupported message type")
