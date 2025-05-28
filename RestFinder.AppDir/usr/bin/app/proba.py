import os
a=[]


def get_available_cities(data_dir="city"):
    """Возвращает список городов из имен файлов в папке city"""
    try:
        # Получаем абсолютный путь к папке city
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, data_dir)

        print(f"[DEBUG] Ищем города в: {data_path}")  # Отладочный вывод

        if not os.path.exists(data_path):
            print(f"[DEBUG] Папка {data_path} не найдена!")
            return []

        cities = []
        for filename in os.listdir(data_path):
            if filename.endswith('.json'):
                city_name = filename[:-5]  # Убираем .json
                cities.append(city_name)
                print(f"[DEBUG] Найден город: {city_name}")  # Отладочный вывод

        return sorted(cities, key=lambda x: x.lower())

    except Exception as e:
        print(f"[ERROR] Ошибка при поиске городов: {e}")
        return []
city = get_available_cities()
for t in city:
    print(t)