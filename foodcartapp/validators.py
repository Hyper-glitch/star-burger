import phonenumbers
from rest_framework.response import Response


def validate_products(raw_order):
    try:
        products = raw_order['products']
    except KeyError as exc:
        products = exc

    match products:
        case str():
            content = {'products': 'Ожидался list со значениями, но был получен str'}
        case None:
            content = {'products': 'Это поле не может быть пустым'}
        case []:
            content = {'products': 'Этот список не может быть пустым'}
        case KeyError():
            content = {'products': 'Обязательное поле'}
        case _:
            serializer = OrderSerializer(data=raw_order)
            serializer.is_valid(raise_exception=True)
            serializer.save(products=products)
            json = JSONRenderer().render(serializer.data)
            return Response(json)


def validate_order(raw_order: dict):
    copied_order = raw_order.copy()
    copied_order.pop('products')
    order_keys = ''
    phonenumber = copied_order.get('phonenumber')
    error_text = None
    content = None

    validate_phone_number(phonenumber)

    if not copied_order:
        order_keys += 'firstname, lastname, phonenumber, address'
        error_text = 'Обязательное поле'
        return {order_keys: error_text}

    for idx, key_value in enumerate(copied_order.items()):
        key, value = key_value
        match value:
            case None | '':
                error_text = 'Это поле не может быть пустым'
                if 0 < idx < len(copied_order.keys()) - 1:
                    order_keys += ', '
                order_keys += f'{key}'
            case []:
                error_text = 'Not a valid string'
                if 0 < idx < len(copied_order.keys()) - 1:
                    order_keys += ', '
                order_keys += f'{key}'

    content = {order_keys: error_text}
    return content


def validate_phone_number(phonenumber):
    parsed_phonenumber = phonenumbers.parse(phonenumber)
    is_phone_valid = phonenumbers.is_valid_number(parsed_phonenumber)
    if not is_phone_valid:
        order_keys = 'phonenumber'
        error_text = 'Введен некорректный номер телефона'
        return {order_keys: error_text}
