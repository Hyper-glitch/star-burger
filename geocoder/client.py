import requests as requests
from geopy import distance
from django.conf import settings


class YandexGeocoderAPI:
    def __init__(self):
        self.base_url = "https://geocode-maps.yandex.ru/1.x"
        self.apikey = settings.YANDEX_GEOCODER_API_KEY

    def fetch_coordinates(self, address: str) -> tuple[float, float]:
        response = requests.get(
            self.base_url,
            params={
                "geocode": address,
                "apikey": self.apikey,
                "format": "json",
            },
        )
        response.raise_for_status()
        found_places = response.json()["response"]["GeoObjectCollection"][
            "featureMember"
        ]
        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
        return float(lon), float(lat)

    @staticmethod
    def calculate_distance(
        order_coords: tuple[float, float], rest_coords: tuple[float, float]
    ) -> str:
        if not any(order_coords):
            return "ошибка определения координат"
        return f"{round(distance.distance(order_coords, rest_coords).km, 3)} км"
