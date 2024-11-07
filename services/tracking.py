import asyncio
import logging
import os
import re

from aiogram.types import Message

from services.api import fetch_page, check_places_available, fetch_page_title

logger = logging.getLogger(__name__)

RELOAD_TIMEOUT_SECONDS = os.getenv("RELOAD_TIMEOUT_SECONDS", 60)


async def start_tracking(message: Message):
    try:
        event_name = fetch_page_title(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await message.answer(f"Started tracking event {event_name}")

    while True:
        bs = fetch_page(message.text)

        logger.info("Tracking... ")

        booking_container = bs.find(id=re.compile("^mec-events-meta-group-booking-[0-9]+$"))

        if check_places_available(booking_container.find(class_="mec-ticket-unavailable-spots")):
            await message.answer(f"Booking available for {event_name}! {message.text}")
            break

        await asyncio.sleep(RELOAD_TIMEOUT_SECONDS)
