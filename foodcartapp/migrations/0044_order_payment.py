# Generated by Django 3.2 on 2023-01-01 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0043_auto_20221226_0734"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.CharField(
                choices=[("CH", "НАЛИЧНЫМИ"), ("OE", "ОНЛАЙН")],
                db_index=True,
                default="CH",
                max_length=2,
                verbose_name="способ оплаты",
            ),
        ),
    ]
