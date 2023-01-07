import phonenumbers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)

from foodcartapp.models import Order, OrderItem


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["firstname", "lastname", "phonenumber", "address"]

    def create(self, validated_data):
        products = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        order_items = [
            OrderItem(
                order=order,
                product=product["product"],
                quantity=product["quantity"],
                price=product["quantity"] * product["product"].price,
            )
            for product in products
        ]
        OrderItem.objects.bulk_create(order_items)
        return order


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ["products", "firstname", "lastname", "phonenumber", "address"]

    def validate_phonenumber(self, phone_number: str):
        if not phonenumbers.is_valid_number(phonenumbers.parse(phone_number)):
            raise ValidationError("Введен некорректный номер телефона")
        return phone_number
