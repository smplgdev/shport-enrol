import re

import requests
from bs4 import BeautifulSoup


def fetch_page_title(webpage_url):
    response = requests.get(webpage_url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch website: %s" % webpage_url)

    return BeautifulSoup(response.content, 'html.parser').title.string.split("-")[0].strip()


def fetch_page(website_url) -> BeautifulSoup:
    response = requests.get(website_url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch website: %s" % website_url)

    return BeautifulSoup(response.content, 'html.parser')


def check_places_available(booking_container):
    if not any("mec-util-hidden" in s for s in booking_container['class']):
        return False
    return True


def check_link(link):
    return re.match(r"https://sportup\.si/dogodki/*", link)
