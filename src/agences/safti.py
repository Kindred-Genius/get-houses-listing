#generic
import time
#Web scrapping
from bs4 import BeautifulSoup
from selenium import webdriver
#project
from helpers import get_text_data, append_csv

BASE_URL = 'https://www.safti.fr'
URL = BASE_URL + '/recherche?project=achat&properties=maison&localities=vernon-27200&page=1&hasRendered=1'
CHROME_DRIVER = "/Users/aba/home/utils/chromedriver/chromedriver"


def get_html():
    driver = webdriver.Chrome(CHROME_DRIVER)
    driver.get(URL)

    time.sleep(2)

    html = driver.page_source

    driver.quit()

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="col-lg-12")

    house_data = []
    for house in house_lists:

        card = house.find('a',
              attrs={'class': lambda e: e.startswith('listItem_cardInner') if e else False})
        
        relative_url = card.get("href")

        house_ref = relative_url.split('/')[-1]

        price, surface, room, bedrooms = get_text_data(card.prettify())
        house_data.append({
            "source": __name__,
            "house_ref": house_ref,
            "url": f'{BASE_URL}{relative_url}',
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