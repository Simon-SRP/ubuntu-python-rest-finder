# def get_rest_places():
#     """Возвращает список мест для отдыха"""
#     return [
#         {
#             "name": "Beach Paradise",
#             "location": "Maldives",
#             "description": "Beautiful beach with white sand and crystal clear water. Perfect for romantic getaways and diving enthusiasts.",
#             "link": "https://example.com/maldives"
#         },
#         {
#             "name": "Mountain Retreat",
#             "location": "Switzerland",
#             "description": "Cozy cabin in the Alps with stunning views. Ideal for skiing in winter and hiking in summer.",
#             "link": "https://example.com/swiss_alps"
#         },
#         {
#             "name": "City Explorer",
#             "location": "Paris, France",
#             "description": "Explore the city of lights with its famous landmarks, museums and cuisine.",
#             "link": "https://example.com/paris"
#         },
#         {
#             "name": "Safari Adventure",
#             "location": "Kenya",
#             "description": "Wildlife safari experience in Masai Mara. See the Big Five in their natural habitat.",
#             "link": "https://example.com/kenya_safari"
#         },
#         {
#             "name": "Tropical Island",
#             "location": "Bali, Indonesia",
#             "description": "Lush jungles, ancient temples and beautiful beaches. A perfect mix of culture and relaxation.",
#             "link": "https://example.com/bali"
#         }
#     ]

# models.py
from .api import AmadeusAPI


def get_hotels():
    """Возвращает отфильтрованный список отелей"""
    amadeus = AmadeusAPI()
    hotels = amadeus.search_hotels(count=50)

    if not hotels:
        # Возвращаем мок-данные при ошибке
        return [{
            "name": f"Пример отеля {i}",
            "address": f"Адрес {i}, Париж",
            "rating": round(4 + (i % 3) / 2, 1),
            "distance": f"{i * 0.5} км"
        } for i in range(1, 51)]

    return [{
        "name": hotel.get("name", "Без названия"),
        "address": hotel.get("address", {}).get("lines", ["Адрес не указан"])[0],
        "rating": hotel.get("rating", "N/A"),
        "distance": f"{hotel.get('distance', {}).get('value', 0)} {hotel.get('distance', {}).get('unit', 'km')}"
    } for hotel in hotels]