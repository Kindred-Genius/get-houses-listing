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

BASE_URL = 'https://www.laref.net'
URL = BASE_URL
CHROME_DRIVER = "/Users/aba/home/utils/chromedriver/chromedriver"

def get_html():

    # the interface for turning on headless mode 
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    driver.get(URL)

    time.sleep(2)

    input_location = driver.find_element(By.XPATH, '/html/body/header/div[2]/div/div[2]/div[2]/div[2]/section/div/form/div[1]/fieldset/div/div/div/div[3]/div[2]/div[1]/input')
    input_location.send_keys('Vernon')
    time.sleep(2)
    input_vernon_location = driver.find_element(By.XPATH, '/html/body/header/div[2]/div/div[2]/div[2]/div[2]/section/div/form/div[1]/fieldset/div/div/div/div[3]/div[2]/div[3]/div/div/div[2]/div[2]/div[2]')
    input_vernon_location.click()
    time.sleep(1)

    input_home_type = driver.find_element(By.XPATH, '/html/body/header/div[2]/div/div[2]/div[2]/div[2]/section/div/form/div[1]/fieldset/div/div/div/div[2]/div/div[1]')
    input_home_type.click()
    time.sleep(1)
    input_home_type_house = driver.find_element(By.CSS_SELECTOR, '.ss-open > div:nth-child(2) > div:nth-child(3)')
    input_home_type_house.click()
    time.sleep(1)

    submit = driver.find_element(By.XPATH, '/html/body/header/div[2]/div/div[2]/div[2]/div[2]/section/div/form/div[2]/button')
    submit.click()
    time.sleep(2)

    html = driver.page_source

    driver.quit()

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("div", class_="property-listing-v1__item item")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a', class_='linkBloc').get("href")
        complete_url = f'{BASE_URL}{relative_url}'
        house_ref = house.find('div', class_='item__info-id').text.split(' ')[-1]
        
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
    init()