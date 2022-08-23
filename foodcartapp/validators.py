import phonenumbers


def validate_products(raw_order):
    product_key = 'products'
    error_text = None

    try:
        products = raw_order['products']
    except KeyError as exc:
        products = exc

    match products:
        case str():
            error_text = 'Ожидался list со значениями, но был получен str'
        case None:
            error_text = 'Это поле не может быть пустым'
        case []:
            error_text = 'Этот список не может быть пустым'
        case KeyError():
            error_text = 'Обязательное поле'

    content = {product_key: error_text}
    return content if error_text else None


def validate_order(raw_order: dict):
    copied_order = raw_order.copy()
    copied_order.pop('products')
    order_keys = ''
    error_text = None
    phonenumber = copied_order.get('phonenumber')

    if not copied_order:
        order_keys += 'firstname, lastname, phonenumber, address'
        error_text = 'Обязательное поле'
        return {order_keys: error_text}

    content = validate_phone_number(phonenumber) if phonenumber else None
    if content:
        return content

    for idx, key_value in enumerate(copied_order.items()):
        key, value = key_value
        match value:
            case None | '':
                error_text = 'Это поле не может быть пустым'
                if 0 < idx:
                    order_keys += ', '
                order_keys += f'{key}'
            case []:
                error_text = 'Not a valid string'
                if 0 < idx:
                    order_keys += ', '
                order_keys += f'{key}'

    content = {order_keys.lstrip(', '): error_text}
    return content if error_text else None


def validate_phone_number(phonenumber: str) -> None | dict:
    parsed_phonenumber = phonenumbers.parse(phonenumber)
    if not phonenumbers.is_valid_number(parsed_phonenumber):
        order_keys = 'phonenumber'
        error_text = 'Введен некорректный номер телефона'
        return {order_keys: error_text}
