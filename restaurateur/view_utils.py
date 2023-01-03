from typing import Any
from django.db.models import QuerySet

from foodcartapp.models import Order, Restaurant
from geocoder.client import YandexGeocoderAPI


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


def intersect_order_restaurants(client: YandexGeocoderAPI, orders: QuerySet) -> None:
    rests = {}
    rests_with_coords = {}

    for order in orders:
        for item in order.items.all():
            product = item.product
            for menu_item in product.menu_items.all():
                if menu_item.availability:
                    restaurant = menu_item.restaurant
                    rests_with_coords.update(
                        {
                            restaurant.pk: client.fetch_coordinates(
                                address=restaurant.address
                            )
                        }
                    )
                else:
                    continue
                if not rests.get(product.pk):
                    rests.update({product.pk: [restaurant]})
                else:
                    rests[product.pk].append(restaurant)

        values = list(rests.values())
        intersected_rests: set[Restaurant] = set.intersection(*map(set, values))
        calculate_order_distances(
            order=order,
            client=client,
            rests=intersected_rests,
            rests_with_coords=rests_with_coords,
        )
        rests = {}


def calculate_order_distances(
    order: Order,
    client: YandexGeocoderAPI,
    rests: set[Restaurant],
    rests_with_coords: dict[int, list[str]],
) -> None:
    order_coords = client.fetch_coordinates(address=order.address)
    rests_distances = {}

    for rest in rests:
        rests_distances[rest] = client.calculate_distance(
            order_coords=order_coords, rest_coords=rests_with_coords[rest.pk]
        )
    order.distances = rests_distances
