from django.db import models
from django.contrib.auth.models import User, auth

# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    availability = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Cart(models.Model):

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Quantity(models.Model):

    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    soldQty = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class ShowCart():

    id: int
    name: str
    qty: int
    price: int
    img: str
    prod_id: int
    unit_price: int
