import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html, _get_local_html

BASE_URL = 'https://www.lesage-immobilier-vernon.com'
P1 = '/index.php?cur_page='
P2 = '&&sortby=Prix&sorttype=ASC&type=Vente&bien=Maisons+-+Proprietes&action=searchresults'

def get_html():
    html = ''
    for i in range(0, 3):
        response = requests.get(url=f'{BASE_URL}{P1}{i}{P2}', headers=HEADERS, timeout=10)
        response.raise_for_status()
        html += response.text
        time.sleep(1)

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("section", {'class':['row0', 'row1']})

    house_data = []
    print('agence lesage, found:', len(house_lists))
    for house in house_lists:

        if house.find('div', class_="statut Vendu par l'agence"): continue
        if house.find('aside', class_='col w10 txtcenter pa1').text.strip() != 'Vernon': continue

        relative_url = house.find('a').get("href")
        complete_url = f'{BASE_URL}/{relative_url}'
        house_ref = relative_url.split('-')[0]
        
        price, surface, room, bedrooms = get_text_data(house.get_text('\n', strip=True))

        house_data.append({
            "source": "lesage",
            "house_ref": house_ref,
            "url": complete_url,
            "price": price,
            "surface": surface,
            "room": room,
            "bedrooms": bedrooms
        })
    append_csv(house_data)

def init():
    html = get_html()
    fetch(html)

if __name__ == "__main__":
    print(__name__)
    init()