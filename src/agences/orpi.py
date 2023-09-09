#generic
import time
#Web scrapping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#project
from conf import FIREFOX_DRIVER
from helpers import get_text_data, append_csv, _serialize_html, _get_local_html

BASE_URL = 'https://www.orpi.com'
URL = BASE_URL + '/recherche/buy?realEstateTypes%5B%5D=maison&locations%5B0%5D%5Bvalue%5D=vernon&locations%5B0%5D%5Blabel%5D=Vernon%20%2827200%29&sort=date-down&layoutType=mixte&recentlySold=false'

def get_html():

    browser_opt = Options()
    browser_opt.add_argument("--window-size=1920,1080")
    driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER)
    driver.get(URL)

    time.sleep(2.5)

    html = driver.page_source

    driver.quit()

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    soup_my_result = soup.find('ul', class_='o-grid u-list-unstyled o-grid--2 o-grid--1@sm')

    house_lists = soup_my_result.find_all("li", class_="o-grid__col u-flex u-flex-column")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a', class_='u-link-unstyled c-overlay__link').get("href")
        complete_url = f'{BASE_URL}{relative_url}'
        house_ref = relative_url.split('-')[-1][:-1]
        
        house_card = house
        
        price, surface, room, bedrooms = get_text_data(house_card.get_text('\n', strip=True))
        house_data.append({
            "source": "orpi",
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
    init()