#generic
import time
#Web scrapping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#project
from helpers import get_text_data, append_csv, _serialize_html, _get_local_html

BASE_URL = 'https://www.orpi.com'
URL = BASE_URL + '/recherche/buy?realEstateTypes%5B%5D=maison&locations%5B0%5D%5Bvalue%5D=vernon&locations%5B0%5D%5Blabel%5D=Vernon%20%2827200%29&sort=date-down&layoutType=mixte&recentlySold=false'
AGENCE = __name__.replace('agences.', '')

def get_html():

    # the interface for turning on headless mode 
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(URL)

    time.sleep(4)

    html = driver.page_source

    _serialize_html(driver.find_element(by=By.XPATH, value="//html").text, 'text.txt')
    _serialize_html(driver.find_element(by=By.XPATH, value="//html").get_attribute('innerHTML'), 'inner.html')
    _serialize_html(driver.find_element(by=By.XPATH, value="//html").get_attribute('outerHTML'), 'outer.html')
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
    # html = get_html()
    html = _get_local_html('outer.html')
    fetch(html)

if __name__ == "__main__":
    init()