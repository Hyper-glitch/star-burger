"""
DEPRECATED.
Used for validate data before DRF serializers.
"""
import phonenumbers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ValidationError

from foodcartapp.models import Product


def validate_raw_order(raw_order):
    errors = []

    products_content = validate_products(raw_order.get("products"))
    if products_content:
        errors.append(products_content)

    order_content = validate_order(raw_order)
    if order_content:
        errors.append(order_content)

    raise ValidationError(detail=errors)


def validate_products(products: list) -> dict | None:
    content = (
        validate_product_pk(products)
        if isinstance(products, list) and len(products) > 0
        else None
    )
    if content:
        return content

    match products:
        case str():
            error_text = "Ожидался list со значениями, но был получен str"
        case None:
            error_text = "Это поле не может быть пустым"
        case []:
            error_text = "Этот список не может быть пустым"
        case KeyError():
            error_text = "Обязательное поле"
        case _:
            error_text = None

    content = {"products": error_text}
    return content if error_text else None


def validate_order(raw_order: dict) -> dict | None:
    copied_order = raw_order.copy()
    copied_order.pop("products")
    order_keys = []
    error_text = None
    phonenumber = copied_order.get("phonenumber")

    if not copied_order:
        order_keys += "firstname, lastname, phonenumber, address"
        error_text = "Обязательное поле"
        return {order_keys: error_text}

    content = validate_phone_number(phonenumber) if phonenumber else None
    if content:
        return content

    for idx, key_value in enumerate(copied_order.items()):
        key, value = key_value
        match value:
            case None | "":
                error_text = "Это поле не может быть пустым"
                order_keys.append(f"{key}")
            case []:
                error_text = "Not a valid string"
                order_keys.append(f"{key}")

    content = {", ".join(order_keys): error_text}
    return content if error_text else None


def validate_phone_number(phonenumber: str) -> None | dict:
    parsed_phonenumber = phonenumbers.parse(phonenumber)
    if not phonenumbers.is_valid_number(parsed_phonenumber):
        order_keys = "phonenumber"
        error_text = "Введен некорректный номер телефона"
        return {order_keys: error_text}


def validate_product_pk(products: list):
    for product in products:
        product_pk = product["product"]
        try:
            Product.objects.get(pk=product_pk)
        except ObjectDoesNotExist:
            error_text = f"Недопустимый первичный ключ {product_pk}"
            return {"products": error_text}
