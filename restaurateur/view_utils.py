from typing import Any


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


def intersect_order_restaurants(orders) -> None:
    restaurants = {}

    for order in orders:
        for item in order.items.all():
            product = item.product
            for menu_item in product.menu_items.all():
                if menu_item.availability:
                    restaurant = menu_item.restaurant
                else:
                    continue
                if not restaurants.get(product.pk):
                    restaurants.update({product.pk: [restaurant]})
                else:
                    restaurants[product.pk].append(restaurant)

        values = list(restaurants.values())
        order.restaurants = set.intersection(*map(set, values))
        restaurants = {}
