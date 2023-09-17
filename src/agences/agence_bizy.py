import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'https://www.agencedebizy.fr'
URL = BASE_URL + '/vente/maisons-villas'
AGENCE = __name__.replace('agences.', '')

def get_html():

    response = requests.get(url=f'{URL}/1', headers=HEADERS, timeout=10)
    response.raise_for_status()
    html = response.text

    time.sleep(1)

    response = requests.get(url=f'{URL}/2', headers=HEADERS, timeout=10)
    response.raise_for_status()
    html += response.text

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("article")

    house_data = []
    print('agence bizy, found:', len(house_lists))
    for house in house_lists:

        relative_url = house.find('a').get("href")
        complete_url = relative_url
        house_ref = house.find('span', class_='productIdArticle dataRefPrice').text.split(' ')[-1]
        
        price, surface, room, bedrooms = get_text_data(house.get_text('\n', strip=True))

        house_data.append({
            "source": AGENCE,
            "house_ref": house_ref,
            "url": complete_url,
            "price": price,
            "surface": surface,
            "room": room,
            "bedrooms": bedrooms
        })
    append_csv(house_data, AGENCE)

def init():
    html = get_html()
    fetch(html)

if __name__ == "__main__":
    print(__name__)
    init()