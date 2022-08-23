from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.serializers import (
    Serializer, ModelSerializer, PrimaryKeyRelatedField, CharField, IntegerField, ListField,
)

from foodcartapp.models import Order, OrderItem, Product


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)

        for item in products:
            OrderItem.objects.create(
                product=Product.objects.get(pk=item['product']),
                quantity=item['quantity'],
                order=order,
            )

        return order


class OrderItemSerializer(Serializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = IntegerField()


class OrderSerializer(Serializer):
    products = OrderItemSerializer(many=True, allow_empty=False)
    firstname = CharField()
    lastname = CharField()
    phonenumber = PhoneNumberField()
    address = CharField()
