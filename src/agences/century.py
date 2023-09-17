
import requests
import time
# from functools import reduce
from bs4 import BeautifulSoup
from conf import HEADERS
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'https://www.century21.fr'
URL = BASE_URL + '/annonces/achat-maison/cpv-27200_vernon'
AGENCE = __name__.replace('agences.', '')

def fetch(url):
    response = requests.get(url=url, headers=HEADERS)
    response.raise_for_status()
    html = response.text
    page_max = 2
    page_curr = 2
    while page_curr <= page_max:
        time.sleep(2)
        response = requests.get(url=f'{url}/page-{page_curr}', headers=HEADERS)
        html += response.text
        page_curr += 1
    
    # _serialize_html(html, 'century21.html')
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="js-the-list-of-properties-list-property")

    house_data = []
    house_refs = {}
    for house in house_lists:
        relative_url = house.find('a', class_='c-the-button').get("href")
        house_ref = relative_url.split('/')[-2]

        # if house_ref in house_refs: continue
        
        house_refs[house_ref] = True
        price, surface, room, bedrooms = get_text_data(house.find("div",
                                                                  class_="c-the-property-thumbnail-with-content__col-right").text)
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