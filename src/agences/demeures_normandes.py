import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'https://auxdemeuresnormandes.com'
URL = BASE_URL + '/recherche-avancee/?type=maison'

def get_html():
    
    print(URL)
    response = requests.get(url=URL, headers=HEADERS)
    response.raise_for_status()
    html = response.text

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="property-inner")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a', class_='property-link').get("href")
        complete_url = relative_url

        price, surface, room, bedrooms = get_text_data(house.get_text('\n', strip=True))
        house_ref = f'111-{price.split(" ")[0]}{surface.split(" ")[0]}'
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
    html = get_html()
    fetch(html)

if __name__ == "__main__":
    init()