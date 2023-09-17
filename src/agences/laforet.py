import requests
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv

BASE_URL = 'https://www.laforet.com'
URL = BASE_URL + '/acheter/rechercher?filter%5Bcities%5D=27681&filter%5Btypes%5D=house'
AGENCE = __name__.replace('agences.', '')

def fetch(url):
    response = requests.get(url=url, headers=HEADERS)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")

    house_lists = soup.find_all("div", class_="apartment-card")
    house_data = []
    for house in house_lists:
        relative_url = house.select_one("a").get("href")
        house_ref = relative_url.split('-')[-1]
        price, surface, room, bedrooms = get_text_data(house.find("div", class_="card-bottom").text)
        house_data.append({
            "source": AGENCE,
            "house_ref": house_ref,
            "url": f'{BASE_URL}{relative_url}',
            "price": price,
            "surface": surface,
            "room": room,
            "bedrooms": bedrooms
        })
    append_csv(house_data, AGENCE)

def init():
    fetch(URL)

if __name__ == "__main__":
    init()
