import re
import requests
import time
from bs4 import BeautifulSoup

# has places
WEBSITE_URL="https://sportup.si/dogodki/skupinski-tek-group-jogging-2/?occurrence=2024-10-28"

# no places available
# WEBSITE_URL="https://sportup.si/dogodki/vadba-za-moc-strength-training-624/?occurrence=2024-10-28"

# registration not open
# WEBSITE_URL="https://sportup.si/dogodki/plezanje-indoor-climbing/?occurrence=2024-10-29"

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

def main(website_url=None):
    if not website_url:
        website_url = input("Enter event link: ")

    is_booking_available = False

    while(True):
        bs = fetch_page(website_url)

        if not bs:
            return

        booking_container = bs.find(id=re.compile("^mec-events-meta-group-booking-[0-9]+$"))

        if not booking_container:
            print("Registration not open yet")
            is_booking_available = False
        elif check_places_available(booking_container.find(class_="mec-ticket-unavailable-spots")):
            print("Places available")
            if (is_booking_available == False):
                is_booking_available = True
                # send notification
        else:
            print("No places available")
            is_booking_available = False
        
        time.sleep(60)

if __name__ == "__main__":
    main(WEBSITE_URL)
