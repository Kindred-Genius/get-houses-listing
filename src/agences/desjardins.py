


import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'https://www.agencedesjardins.fr'
URL = BASE_URL + '/ventes/?filters=ville[21]|type-de-bien[217]'

def fetch(url):
    response = requests.get(url=url, headers=HEADERS)
    response.raise_for_status()
    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("li", class_="product")

    house_data = []
    house_refs = {}
    for house in house_lists:
        relative_url = house.find('a', class_='woocommerce-LoopProduct-link').get("href")
        complete_url = relative_url
        house_ref = '3110'

        # if house_ref in house_refs: continue
        
        house_refs[house_ref] = True
        price, surface, room, bedrooms = get_text_data(house.text)
        house_data.append({
            "source": __name__,
            "house_ref": house_ref,
            "url": complete_url,
            "price": price,
            "surface": surface,
            "room": room,
            "bedrooms": bedrooms
        })
    append_csv(house_data, __name__)

def init():
    fetch(URL)

if __name__ == "__main__":
    init()