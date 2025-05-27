import json
import os


def get_hotels(city_name):
    """Загружает все отели для указанного города из файла"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        city_file = os.path.join(current_dir, "city", f"{city_name}.json")

        if not os.path.exists(city_file):
            return []

        with open(city_file, 'r', encoding='utf-8') as f:
            hotels = json.load(f)

            # Проверяем и чистим данные
            valid_hotels = []
            for hotel in hotels:
                if not isinstance(hotel, dict):
                    continue

                # Проверяем обязательные поля
                if 'name' not in hotel or not hotel['name']:
                    continue

                # Устанавливаем значения по умолчанию
                hotel.setdefault('rating', 'N/A')
                hotel.setdefault('distance', 'N/A')
                hotel.setdefault('address', 'Адрес не указан')
                hotel.setdefault('description', 'Описание отсутствует')
                hotel.setdefault('image_url', '')
                hotel.setdefault('hotel_url', '')

                valid_hotels.append(hotel)

            return valid_hotels

    except Exception as e:
        print(f"Ошибка загрузки файла {city_name}.json: {e}")
        return []

