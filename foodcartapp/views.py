from django.http import JsonResponse
from django.templatetags.static import static

from .models import Product, OrderItem
from .schemas import OrderDBSchema, OrderJSONSchema


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    order_json_schema = OrderJSONSchema()
    order_db_schema = OrderDBSchema()

    order = order_json_schema.loads(request.body.decode())
    products = order.pop('products')
    order_obj = order_db_schema.load(order)

    for product_data in products:
        product = Product.objects.get(pk=product_data['product'])
        OrderItem.objects.create(product=product, quantity=product_data['quantity'], order=order_obj)

    return JsonResponse(order)
