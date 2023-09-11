import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'https://vernon.arthurimmo.com'
URL = BASE_URL + '/recherche,basic.htm?transactions=acheter&localization=Vernon+%2827200%29&types%5B%5D=maison&max_price=&min_surface='

def get_html():

    response = requests.get(url=URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    html = response.text

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="relative z-0 flex flex-col h-full justify-between")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a').get("href")
        complete_url = relative_url
        house_ref = relative_url.split('/')[-1][:-4]
        
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
    print(__name__)
    init()