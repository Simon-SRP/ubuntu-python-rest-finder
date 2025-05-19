import requests
import os
from base64 import b64encode
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

class AmadeusAPI:
    def __init__(self):
        self.client_id = os.getenv("AMADEUS_CLIENT_ID", "")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET", "")
        self.base_url = "https://test.api.amadeus.com/v1"
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        try:
            auth_str = f"{self.client_id}:{self.client_secret}"
            auth_b64 = b64encode(auth_str.encode()).decode()

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {auth_b64}"
            }

            response = requests.post(
                "https://test.api.amadeus.com/v1/security/oauth2/token",
                headers=headers,
                data="grant_type=client_credentials"
            )

            # Добавьте отладку
            print("Status Code:", response.status_code)
            print("Response:", response.text)

            response.raise_for_status()
            return response.json()["access_token"]

        except Exception as e:
            print(f"Ошибка при получении токена: {e}")
            return None

    def search_hotels(self, city_code="PAR", count=50):
        if not self.access_token:
            return []

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            params = {
                "cityCode": city_code,
                "radius": 50,
                "radiusUnit": "KM",
                "hotelSource": "ALL"
            }

            response = requests.get(
                f"{self.base_url}/reference-data/locations/hotels/by-city",
                headers=headers,
                params=params
            )

            response.raise_for_status()
            data = response.json()

            return [
                       hotel for hotel in data.get("data", [])
                       if not any(x in hotel.get("name", "").upper()
                                  for x in ["TEST", "PROPERTY"])
                   ][:count]

        except Exception as e:
            print(f"Ошибка при поиске отелей: {e}")
            return []