# Generated by Django 3.2 on 2022-12-26 07:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0042_alter_orderitem_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="called_at",
            field=models.DateTimeField(
                db_index=True, null=True, verbose_name="время подтверждения"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="comment",
            field=models.TextField(
                blank=True, default="", max_length=512, verbose_name="комментарий"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(
                db_index=True,
                default=django.utils.timezone.now,
                verbose_name="время создания",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="delivered_at",
            field=models.DateTimeField(
                db_index=True, null=True, verbose_name="время доставки"
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("UN", "НЕОБРАБОТАННО"),
                    ("PG", "В СБОРКЕ"),
                    ("DV", "В ДОСТАВКЕ"),
                    ("CM", "ГОТОВО"),
                ],
                db_index=True,
                default="UN",
                max_length=120,
                verbose_name="статус",
            ),
        ),
    ]
