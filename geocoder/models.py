from django.utils import timezone

from django.db import models


class Place(models.Model):
    address = models.CharField(
        "адрес",
        max_length=100,
        blank=True,
        unique=True,
    )
    latitude = models.FloatField(max_length=6, verbose_name=" Широта")
    longitude = models.FloatField(max_length=6, verbose_name=" Долгота")
    requested_at = models.DateTimeField(
        verbose_name="Дата запроса", default=timezone.now
    )

    def __str__(self):
        return f"{self.address}, Широта: {self.latitude}, Долгота: {self.longitude}"
