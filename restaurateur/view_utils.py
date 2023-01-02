from typing import Any

from foodcartapp.models import Order


def set_order_total_prices(items):
    pk_prices = count_total_prices(items)
    orders = Order.objects.all()
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
