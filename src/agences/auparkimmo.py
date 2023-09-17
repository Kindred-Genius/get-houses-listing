import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'http://www.auparkimmo.com'
URL = BASE_URL + '/asp/univers2.asp?idU='
AGENCE = __name__.replace('agences.', '')

def get_html():

    html = ''
    for page in range(19, 23):
        paged_url = f'{URL}{page}'
        response = requests.get(url=paged_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        html += response.text
        time.sleep(1)
    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="bien")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a').get("href")
        complete_url = f'{BASE_URL}{relative_url}'
        house_ref = relative_url.split('idB=')[1][:-7]
        
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
    init()