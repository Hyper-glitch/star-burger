from typing import Any

from django.db.models import QuerySet

from foodcartapp.models import Order, Restaurant
from geocoder.client import YandexGeocoderAPI
from geocoder.models import Place


def set_order_total_prices(orders, items):
    pk_prices = count_total_prices(items)
    for order in orders:
        order.total_price = pk_prices[order.pk]
    return orders


def count_total_prices(items) -> dict[str, Any]:
    pk_prices: dict[str, Any] = {}
    for pk, total_price in items:
        if not pk_prices.get(pk):
            pk_prices.update({pk: total_price})
        else:
            pk_prices[pk] += total_price
    return pk_prices


def intersect_order_restaurants(
    client: YandexGeocoderAPI, orders: QuerySet, places
) -> None:
    rests = {}
    places_to_create = []

    for order in orders:
        address = order.address
        if address not in places:
            add_place_to_create(client, address, places_to_create, places)

        for item in order.items.all():
            product = item.product
            for menu_item in product.menu_items.all():
                if menu_item.availability:
                    restaurant = menu_item.restaurant
                else:
                    continue
                if not rests.get(product.pk):
                    rests.update({product.pk: [restaurant]})
                else:
                    rests[product.pk].append(restaurant)

        values = list(rests.values())
        intersected_rests: set[Restaurant] = set.intersection(*map(set, values))
        calculate_order_distances(
            places_to_create=places_to_create,
            order=order,
            places=places,
            client=client,
            rests=intersected_rests,
        )
        rests = {}

    Place.objects.bulk_create(places_to_create)

def calculate_order_distances(
    places_to_create: list,
    order: Order,
    places: dict[str, tuple[float, float]],
    client: YandexGeocoderAPI,
    rests: set[Restaurant],
) -> None:
    rests_distances = {}

    for rest in rests:
        address = rest.address
        if address not in places:
            add_place_to_create(client, address, places_to_create, places)

        rests_distances[rest] = client.calculate_distance(
            order_coords=places[order.address],
            rest_coords=places[address],
        )
    order.distances = rests_distances


def get_places(orders: QuerySet, rests: QuerySet)-> dict[str, tuple[float, float]]:
    addresses = list(rests.values_list("address", flat=True))
    addresses.extend(list(orders.values_list("address", flat=True)))
    places = {
        place.address: (place.longitude, place.latitude)
        for place in Place.objects.filter(address__in=addresses)
    }
    return places


def add_place_to_create(client: YandexGeocoderAPI, address: str, places_to_create: list, places: dict[str, tuple[float, float]]):
    longitude, latitude = client.fetch_coordinates(address=address)
    places_to_create.append(
        Place(address=address, latitude=latitude, longitude=longitude)
    )
    places[address] = (longitude, latitude)
