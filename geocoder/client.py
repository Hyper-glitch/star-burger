import requests as requests
from geopy import distance
from star_burger.settings import YANDEX_GEOCODER_API_KEY


class YandexGeocoderAPI:
    def __init__(self):
        self.base_url = "https://geocode-maps.yandex.ru/1.x"
        self.apikey = YANDEX_GEOCODER_API_KEY

    def fetch_coordinates(self, address: str):
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
        return most_relevant["GeoObject"]["Point"]["pos"].split(" ")

    @staticmethod
    def calculate_distance(
        order_coords: list[str, str], rest_coords: list[str, str]
    ) -> float:
        return round(distance.distance(order_coords, rest_coords).km, 3)
