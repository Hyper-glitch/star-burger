# Generated by Django 2.2.5 on 2020-09-28 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0033_auto_20200928_1930"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(blank=True, max_length=200, verbose_name="описание"),
        ),
    ]
