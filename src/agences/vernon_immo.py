import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'https://vernon-immobilier.fr'
URL = BASE_URL + '/biens?categorie=2&prixMinimum=220000&prixMaximum=420000'

def get_html():
    
    response = requests.get(url=URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    html = response.text

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="single-bien")

    house_data = []
    for house in house_lists:

        house_ref = house.find('div', class_='col-md-5 col-lg-3 text-right order-md-1').text.split(' ')[-1]
        relative_url = f'/biens/{house_ref}'
        complete_url = f'{BASE_URL}{relative_url}'
        price, surface, room, bedrooms = get_text_data(house.get_text('\n', strip=True))

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