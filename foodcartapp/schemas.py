"""Module for serialization models for foodcartapp."""
from marshmallow import Schema, fields, validates, ValidationError, post_load

from foodcartapp.models import Order


class OrderItemJSONSchema(Schema):
    """Schema for serialization items information."""
    product = fields.Integer()
    quantity = fields.Integer()


class OrderJSONSchema(Schema):
    """Schema for serialization order information."""
    firstname = fields.Str()
    lastname = fields.Str()
    phonenumber = fields.Str()
    address = fields.Str()
    products = fields.Nested(OrderItemJSONSchema, many=True, only=('product', 'quantity'))

    @validates('products')
    def validate_length(self, value):
        if len(value) < 1:
            raise ValidationError('Quantity must be greater than 0.')


class OrderDBSchema(Schema):
    firstname = fields.Str()
    lastname = fields.Str()
    phonenumber = fields.Str()
    address = fields.Str()

    @post_load
    def make_order(self, data, **kwargs):
        return Order.objects.create(**data)
