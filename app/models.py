from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    money = models.PositiveIntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    num = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Refund(models.Model):
    ref = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

