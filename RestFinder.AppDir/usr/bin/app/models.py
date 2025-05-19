from .api import AmadeusAPI, EUROPEAN_CAPITALS


def get_hotels(count=50, city_code="PAR"):
    amadeus = AmadeusAPI()
    hotels = amadeus.search_hotels(count=count,city_code=city_code)

    if not hotels:
        return [{
            "name": f"Пример отеля {i}",
            "address": f"Адрес {i}, {list(EUROPEAN_CAPITALS.keys())[list(EUROPEAN_CAPITALS.values()).index(city_code)]}",
            "rating": round(4 + (i % 3) / 2, 1),
            "distance": f"{i * 0.5} км"
        } for i in range(1, count+1)]

    return [{
        "name": hotel.get("name", "Без названия"),
        "address": hotel.get("address", {}).get("lines", ["Адрес не указан"])[0],
        "rating": hotel.get("rating", "N/A"),
        "distance": f"{hotel.get('distance', {}).get('value', 0)} {hotel.get('distance', {}).get('unit', 'km')}"
    } for hotel in hotels]