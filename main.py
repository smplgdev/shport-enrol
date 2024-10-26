import os
import re
import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from datetime import datetime

load_dotenv()

TG_BOT_API_TOKEN = os.getenv("TG_BOT_API_TOKEN")

bot = Bot(TG_BOT_API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

dp = Dispatcher()

def fetch_page(website_url):
    response = requests.get(website_url)
    if response.status_code != 200:
        print(f"Failed to fetch website: {website_url}")
        return

    return BeautifulSoup(response.content, 'html.parser')


def check_places_available(booking_container):
    if not any("mec-util-hidden" in s for s in booking_container['class']):
        return False 
    return True

def check_link(link):
    return re.match(r"https://sportup.si/dogodki/.*", link)

async def start_tracking(message):
    is_booking_available = False

    bs = fetch_page(message.text)

    if not bs:
        return

    event_name = bs.title.string.split("-")[0].strip()
    await message.answer("Started tracking event " + event_name)

    while True:
        bs = fetch_page(message.text)

        print("Tracking... " + datetime.now().strftime("%H:%M:%S"))

        if not bs:
            return

        event_name = bs.title.string.split("-")[0].strip()

        booking_container = bs.find(id=re.compile("^mec-events-meta-group-booking-[0-9]+$"))

        if not booking_container:
            is_booking_available = False
        elif check_places_available(booking_container.find(class_="mec-ticket-unavailable-spots")):
            if (is_booking_available == False):
                is_booking_available = True
                await message.answer(f"Booking available for {event_name}! {message.text}")
        else:
            is_booking_available = False
        
        time.sleep(60)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello! Send me the link to the event you want to track")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        if check_link(message.text):
            await start_tracking(message)
        else:
            await message.answer("Invalid link")
    except TypeError:
        await message.answer("Unsupported message type")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
