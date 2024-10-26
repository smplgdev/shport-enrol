import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

WEBSITE_URL = os.getenv("WEBSITE_URL")


def main():
    response = requests.get(WEBSITE_URL)
    if response.status_code != 200:
        print(f"Failed to fetch website: {WEBSITE_URL}")
        return

    bs = BeautifulSoup(response.content, 'html.parser')

    print(bs.prettify())


if __name__ == "__main__":
    main()
