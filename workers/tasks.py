import asyncio
import re

from aiogram.exceptions import AiogramError

from db.commands import get_events, delete_event
from main import bot
from services.api import fetch_page, is_available_for_booking
from workers.celery_app import app, logger, TELEGRAM_ID_WHITE_LIST, session

SENDING_MESSAGES_DELAY = 1/30


def async_task(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func(*args, **kwargs))


async def send_notification(name, link):
    logger.debug(TELEGRAM_ID_WHITE_LIST)
    for user_id in TELEGRAM_ID_WHITE_LIST:
        if user_id == "":
            continue
        logger.debug("Sending message to %s" % user_id)
        try:
            await bot.send_message(user_id, text=f"Booking available for {name}! {link}")
        except AiogramError as e:
            logger.error(e)
        await asyncio.sleep(SENDING_MESSAGES_DELAY)
        logger.debug("Sleeep???")


@app.task(name='scan_events')
def scan_events():
    events = get_events(session)

    logger.info("Scanning %i event%s..." % (len(events), "" if len(events) == 1 else "s"))
    for event in events:
        _id, name, link, _ = event

        bs = fetch_page(link)

        booking_container = bs.find(id=re.compile("^mec-events-meta-group-booking-[0-9]+$"))

        if not booking_container:
            continue

        if is_available_for_booking(booking_container.find(class_="mec-ticket-unavailable-spots")):
            logger.info(f"Booking available for {name}! {link}")
            async_task(send_notification, name=name, link=link)
            delete_event(session, event_id=_id)
