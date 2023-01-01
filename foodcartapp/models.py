from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import F
from django.utils.translation import gettext_lazy as _


class Restaurant(models.Model):
    name = models.CharField("название", max_length=50)
    address = models.CharField(
        "адрес",
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        "контактный телефон",
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "рестораны"

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = RestaurantMenuItem.objects.filter(availability=True).values_list(
            "product"
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField("название", max_length=50)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("название", max_length=50)
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="категория",
        related_name="products",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        "цена", max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    image = models.ImageField("картинка")
    special_status = models.BooleanField(
        "спец.предложение",
        default=False,
        db_index=True,
    )
    description = models.TextField(
        "описание",
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="menu_items",
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="продукт",
    )
    availability = models.BooleanField("в продаже", default=True, db_index=True)

    class Meta:
        verbose_name = "пункт меню ресторана"
        verbose_name_plural = "пункты меню ресторана"
        unique_together = [["restaurant", "product"]]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        UNREFINED = "UN", _("НЕОБРАБОТАННО")
        PACKING = "PG", _("В СБОРКЕ")
        DELIVERING = "DV", _("В ДОСТАВКЕ")
        COMPLETED = "CM", _("ГОТОВО")

    class Payment(models.TextChoices):
        CASH = "CH", _("НАЛИЧНЫМИ")
        ONLINE = "OE", _("ОНЛАЙН")

    firstname = models.CharField("Имя", max_length=50)
    lastname = models.CharField("Фамилия", max_length=50)
    phonenumber = PhoneNumberField("Телефон", db_index=True)
    address = models.CharField(
        verbose_name="Адрес доставки", max_length=120, db_index=True
    )
    status = models.CharField(
        "статус",
        max_length=120,
        choices=Status.choices,
        default=Status.UNREFINED,
        db_index=True,
    )
    payment = models.CharField(
        "способ оплаты",
        max_length=2,
        choices=Payment.choices,
        default=Payment.CASH,
        db_index=True,
    )
    comment = models.TextField(
        "комментарий",
        max_length=512,
        default="",
        blank=True,
    )
    created_at = models.DateTimeField(
        "время создания", default=timezone.now, db_index=True
    )
    called_at = models.DateTimeField("время подтверждения", db_index=True, null=True)
    delivered_at = models.DateTimeField("время доставки", db_index=True, null=True)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.address}"


class OrderItemQuerySet(models.QuerySet):
    def total_price(self):
        return self.select_related("product").annotate(
            total_price=(F("quantity") * F("product__price"))
        )


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="продукт",
    )
    quantity = models.IntegerField(verbose_name="количество")
    order = models.ForeignKey(
        Order,
        related_name="items",
        verbose_name="заказ",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        "стоимость",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
    )
    objects = OrderItemQuerySet.as_manager()

    class Meta:
        verbose_name = "элемент заказа"
        verbose_name_plural = "элементы заказа"

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
