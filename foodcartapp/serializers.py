import phonenumbers
from rest_framework.serializers import (
    Serializer, ModelSerializer, PrimaryKeyRelatedField, CharField, IntegerField, ValidationError,
)

from foodcartapp.models import Order, OrderItem, Product


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        order_items = [
            OrderItem(order=order, product=product['product'], quantity=product['quantity']) for product in products
        ]
        return OrderItem.objects.bulk_create(order_items)


class OrderItemSerializer(Serializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = IntegerField()


class OrderSerializer(Serializer):
    products = OrderItemSerializer(many=True, allow_empty=False)
    firstname = CharField()
    lastname = CharField()
    phonenumber = CharField()
    address = CharField()

    def validate_phonenumber(self, phonenumber: str):
        parsed_phonenumber = phonenumbers.parse(phonenumber)
        if not phonenumbers.is_valid_number(parsed_phonenumber):
            raise ValidationError('Введен некорректный номер телефона')
        return phonenumber
