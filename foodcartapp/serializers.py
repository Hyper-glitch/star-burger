from rest_framework import serializers

from foodcartapp.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address'],
        )
        return order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def create(self, validated_data):
        order_item = OrderItem.objects.create(
            product=validated_data['product'],
            quantity=validated_data['quantity'],
            order=validated_data['order'],
        )
        return order_item
