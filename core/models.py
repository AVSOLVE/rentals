from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Item(TimeStampedModel):
    name = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Rental(TimeStampedModel):

    PERIOD_CHOICES = [
        ("matutino", "MATUTINO"),
        ("vespertino", "VESPERTINO"),
    ]

    CLASSES_CHOICES = [
        ("1 aula", "1ª AULA"),
        ("2 aula", "2ª AULA"),
        ("3 aula", "3ª AULA"),
        ("4 aula", "4ª AULA"),
        ("5 aula", "5ª AULA"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=False)
    period = models.CharField(
        choices=PERIOD_CHOICES, max_length=20, null=True, blank=False
    )
    period_time = models.CharField(
        choices=CLASSES_CHOICES, max_length=20, null=True, blank=False
    )
    room = models.CharField(max_length=100, null=True, blank=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        client_name = self.client.username if self.client else "Unknown"
        return f"{self.item.name} solicitado por {client_name} para o dia {self.date} no período {self.period} na sala {self.room}"
