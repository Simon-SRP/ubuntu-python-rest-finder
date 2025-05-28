import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def get_available_cities(data_dir="city"):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, data_dir)

        print(f"[DEBUG] Ищем города в: {data_path}")

        if not os.path.exists(data_path):
            print(f"[DEBUG] Папка {data_path} не найдена!")
            return []

        cities = []
        for filename in os.listdir(data_path):
            if filename.endswith('.json'):
                city_name = filename[:-5]  # Убираем .json
                cities.append(city_name)
                print(f"[DEBUG] Найден город: {city_name}")

        return sorted(cities, key=lambda x: x.lower())

    except Exception as e:
        print(f"[ERROR] Ошибка при поиске городов: {e}")
        return []


class BookingParser:
    def __init__(self):
        self.driver = None
        self.data_dir = "city"
        os.makedirs(self.data_dir, exist_ok=True)

    def _init_driver(self):
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/90.0.4430.212 Safari/537.36")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

    def search_hotels(self, city_name):
        city_file = os.path.join(self.data_dir, f"{city_name}.json")

        self._init_driver()
        url = f'https://www.booking.com/searchresults.ru.html?ss={city_name}'
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]')))
        except Exception as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return []

        hotels = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        hotels_data = []

        for hotel in hotels:
            hotel_info = {
                'name': self._get_element_text(hotel, 'div[data-testid="title"]'),
                'rating': self._get_rating(hotel),
                'address': self._get_element_text(hotel, '[data-testid="address"]'),
                'distance': self._get_element_text(hotel, '[data-testid="distance"]'),
                'description': self._get_element_text(hotel, '[data-testid="property-description"]'),
                'image_url': self._get_attribute(hotel, 'img[data-testid="image"]', 'src'),
                'hotel_url': self._get_attribute(hotel, 'a[data-testid="title-link"]', 'href')
            }
            hotels_data.append(hotel_info)

        with open(city_file, 'w', encoding='utf-8') as f:
            json.dump(hotels_data, f, ensure_ascii=False, indent=2)

        return hotels_data

    def _get_element_text(self, parent, *selectors):
        for selector in selectors:
            try:
                return parent.find_element(By.CSS_SELECTOR, selector).text.strip()
            except:
                continue
        return "N/A"

    def _get_attribute(self, parent, selector, attribute):
        try:
            return parent.find_element(By.CSS_SELECTOR, selector).get_attribute(attribute)
        except:
            return "N/A"

    def _get_rating(self, parent):
        try:
            rating_element = parent.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]')
            return rating_element.text.split('\n')[0].strip()
        except:
            return "N/A"

    def close(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def __del__(self):
        self.close()