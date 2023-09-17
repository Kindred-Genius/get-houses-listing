#generic
import time
#Web scrapping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#project
from conf import FIREFOX_DRIVER
from helpers import get_text_data, append_csv, _serialize_html

BASE_URL = 'https://www.stephaneplazaimmobilier.com'
URL = BASE_URL + '/immobilier-acheter?type=2&location=27681&now=1&page=2'
AGENCE = __name__.replace('agences.', '')

def get_html():
    # the interface for turning on headless mode 
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(URL)

    time.sleep(4)

    html = driver.page_source
    driver.quit()

    return html


def fetch(html):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="purchase")

    house_data = []
    house_refs = {}
    for house in house_lists:
        relative_url = house.find('a', class_='suggestion-link').get("href")
        house_ref = relative_url.split('/')[2]

        #TODO: check if validating ref is necessary
        # if house_ref in house_refs: continue
        
        house_refs[house_ref] = True
        price, surface, room, bedrooms = get_text_data(house.text)
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
    html = get_html()
    fetch(html)

if __name__ == "__main__":
    init()