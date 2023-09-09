#generic
import time
#Web scrapping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#project
from helpers import get_text_data, append_csv, _serialize_html, _get_local_html

BASE_URL = 'https://www.ifcconseils.fr'
URL = BASE_URL
CHROME_DRIVER = "/Users/aba/home/utils/chromedriver/chromedriver"

def get_html():

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
    driver.get(URL)

    time.sleep(3.5)
    
    button_search = driver.find_element(By.ID, 'getCloseCookies')
    button_search.click()
    time.sleep(1)

    button_search = driver.find_element(By.ID, 'search-toggle')
    button_search.click()
    time.sleep(1)

    input_location = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[1]/div[2]/div/div/div/form/div[1]/div/fieldset/div/div/div[1]/div[3]/div[2]/div[1]/input')
    input_location.send_keys('Vernon')
    time.sleep(2)
    input_vernon_location = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[1]/div[2]/div/div/div/form/div[1]/div/fieldset/div/div/div[1]/div[3]/div[2]/div[3]/div/div/div[2]/div[2]/div[2]')
    input_vernon_location.click()
    time.sleep(1)

    input_home_type = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[1]/div[2]/div/div/div/form/div[1]/div/fieldset/div/div/div[1]/div[2]/div/div[1]')
    input_home_type.click()
    time.sleep(1)
    lov_house_type = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[1]/div[2]/div/div/div/form/div[1]/div/fieldset/div/div/div[1]/div[2]/div/div[2]/div[2]')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 2", lov_house_type)
    time.sleep(1)
    input_home_type_house = driver.find_element(By.CSS_SELECTOR, '.ss-open > div:nth-child(2) > div:nth-child(4)')
    input_home_type_house.click()
    time.sleep(1)

    form_scroller = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[1]/div[2]/div/div')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 2", form_scroller)
    time.sleep(1)
    submit = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[1]/div[2]/div/div/div/form/div[2]/button')
    submit.click()
    time.sleep(2)

    html = driver.page_source
    driver.quit()

    return html

def fetch(html='test'):
    
    soup = BeautifulSoup(html, "html.parser")

    house_lists = soup.find_all("article", class_="property-listing-v1__item item js-animate")

    house_data = []
    for house in house_lists:

        relative_url = house.find('a', class_='decorate__hover-text js-obfuscation').get("href")
        house_ref = house.find('div', class_='item__reference').text.split(' ')[-1]
        
        house_card = house.find('div', class_='item__block-text')
        
        price, surface, room, bedrooms = get_text_data(house_card.text)
        house_data.append({
            "source": "ifc-conseil",
            "house_ref": house_ref,
            "url": f'{BASE_URL}{relative_url}',
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