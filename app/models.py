from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    money = models.DecimalField(max_digits=9, decimal_places=2, default=10000, verbose_name='Money')


class Product(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    stock = models.PositiveIntegerField()

    class Meta:
        ordering = ['-id', ]


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    num = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', ]


class Refund(models.Model):

    ref = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', ]

