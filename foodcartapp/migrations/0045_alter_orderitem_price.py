# Generated by Django 3.2 on 2023-01-03 12:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0044_order_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="общая стоимость",
            ),
        ),
    ]
