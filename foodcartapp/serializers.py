from rest_framework import serializers

from foodcartapp.models import Order, OrderItem, Product


class OrderSerializer(serializers.ModelSerializer):
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
