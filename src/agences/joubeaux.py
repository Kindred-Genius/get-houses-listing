#generic
import time
#Web scrapping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#project
from conf import FIREFOX_DRIVER
from helpers import get_text_data, append_csv, _get_local_html

BASE_URL = 'https://www.joubeaux-immobilier.com'
URL = BASE_URL

def get_html():
    # the interface for turning on headless mode 
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(URL)

    time.sleep(3)

    input_location = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div[2]/div[2]/section/div/form/div[1]/fieldset/div/div/div/div[4]/div[2]/div[1]/input')
    input_location.send_keys('Vernon')
    time.sleep(3)
    input_vernon_location = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div[2]/div[2]/section/div/form/div[1]/fieldset/div/div/div/div[4]/div[2]/div[3]/div/div/div[2]/div[2]/div[2]')
    input_vernon_location.click()
    time.sleep(1)
    input_home_type = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div[2]/div[2]/section/div/form/div[1]/fieldset/div/div/div/div[2]/div/div[1]')
    input_home_type.click()
    time.sleep(1)
    lov_house_type = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div[2]/div[2]/section/div/form/div[1]/fieldset/div/div/div/div[2]/div/div[2]/div[2]')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", lov_house_type)
    time.sleep(1)
    input_home_type_house = driver.find_element(By.CSS_SELECTOR, '.ss-open > div:nth-child(2) > div:nth-child(5)')
    input_home_type_house.click()
    time.sleep(1)

    submit = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div[2]/div[2]/section/div/form/div[2]/button')
    submit.click()
    time.sleep(2)

    html = driver.page_source
    time.sleep(1)

    current_url = driver.current_url

    driver.get(current_url + '2')
    
    html += driver.page_source
    driver.quit()
    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="property-listing-v1__item item")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a', class_='linkBloc').get("href")
        house_ref = house.find('div', class_='item__info-id').text.split(' ')[-1]
        
        house_card = house.find('div', class_='item__data')
        
        price, surface, room, bedrooms = get_text_data(house_card.text)
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