#generic
import time
#Web scrapping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
#project
from helpers import get_text_data, append_csv

BASE_URL = 'https://www.squarehabitat.fr/'
URL = BASE_URL
AGENCE = __name__.replace('agences.', '')

def get_html():
    # the interface for turning on headless mode 
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    driver.get(URL)

    time.sleep(5)

    try: privacy_btn = driver.find_element(By.ID, 'popin_tc_privacy_button')
    except NoSuchElementException: print('No privacy window detected...')
    else:
        privacy_btn.click()
        time.sleep(1)
    
    input_location = driver.find_element(By.ID, 'cphContent_ctl00_txtGeoloc1A')
    input_location.send_keys('Vernon')
    time.sleep(1)
    input_location.send_keys(Keys.ENTER)
    time.sleep(1)
    input_home_title = driver.find_element(By.XPATH, '/html/body/form/div[3]/section[1]/div/div[2]/div/p')
    input_home_title.click()
    time.sleep(1)
    input_home_type = driver.find_element(By.XPATH, '/html/body/form/div[3]/section[1]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/div')
    input_home_type.click()
    time.sleep(1)
    input_home_type_house = driver.find_element(By.XPATH, '/html/body/form/div[3]/section[1]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/ul/li[2]/a')
    input_home_type_house.click()
    time.sleep(1)

    submit = driver.find_element(By.ID, 'cphContent_ctl00_lnkRechercher')
    submit.click()
    time.sleep(2)

    html = driver.page_source

    driver.quit()

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="blog-post")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a', class_='photo-bien').get("href")
        house_ref = relative_url.split('-')[-1][:-5]
        
        house_card = house.find('div', class_='blog-details')
        
        price, surface, room, bedrooms = get_text_data(house_card.text)
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