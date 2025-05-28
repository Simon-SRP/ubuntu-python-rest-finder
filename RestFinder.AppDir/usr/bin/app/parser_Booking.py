from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriver, ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import random

search_query = ('Торонто')

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/90.0.4430.212 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

url = f'https://www.booking.com/searchresults.ru.html?ss={search_query}'
driver.get(url)

hotels_data = []


WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]'))
)
print('Страница загружена')

def scroll_page():
    last_height = driver.execute_script('return document.body.scrollHeight')
    scroll_attempt = 0
    while scroll_attempt < 5:
        for i in range(1, 5):
            driver.execute_script(f'window.scrollTo(0, document.body.scrollHeight/{5 - i});')
            time.sleep(random.uniform(0.3, 0.7))
        time.sleep(random.uniform(1.5, 3.0))
        new_height = driver.execute_script('return document.body.scrollHeight')


        if new_height == last_height:
            break
        last_height = new_height
        scroll_attempt += 1
        print(f'Прокрутка {scroll_attempt}/5')

scroll_page()

hotels = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
print(f'Найдено отелей: {len(hotels)}')
for i, hotel in enumerate(hotels, 1):
    hotels_info = {
        'name': 'N/A',
        'rating': 'N/A',
        'address': 'N/A',
        'distance': 'Неизвестно, насколько далеко этот отель от центра города',
        'description': 'Описания нет',
        'image_url': 'N/A',
        'hotel_url': 'N/A'
    }
    try:
        hotels_info['name'] = hotel.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
    except:
        pass

    try:
        hotels_info['rating'] = hotel.find_element(By.CSS_SELECTOR,
                                                   'div[data-testid="review-score"]').text.split('\n')[0]
    except:
        pass

    try:
        hotels_info['address'] = hotel.find_element(By.CSS_SELECTOR, '[data-testid="address"]').text

    except:
        pass

    try:
        hotels_info['distance'] = hotel.find_element(By.CSS_SELECTOR, 'span[data-testid="distance"]').text
    except:
        pass

    try:
        hotels_info['description'] = hotel.find_element(By.CSS_SELECTOR, '[class="fff1944c52"]').text
    except:
        pass

    try:
        hotels_info['image_url'] = hotel.find_element(By.CSS_SELECTOR,
                                                      'img[data-testid="image"]').get_attribute('src')
    except:
        pass

    try:
        hotels_info['hotel_url'] = hotel.find_element(By.CSS_SELECTOR,
                                                      'a[data-testid="title-link"]').get_attribute('href')
    except:
        pass

    hotels_data.append(hotels_info)

print(hotels_data)
with open(f'city/{search_query}.json', 'w', encoding='UTF-8') as f:
    json.dump(hotels_data, f, indent=2)

