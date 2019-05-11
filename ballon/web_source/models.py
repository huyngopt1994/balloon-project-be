from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=255)
    telephone = models.IntegerField()
    tax_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Products(models.Model):
    price = models.IntegerField()
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Discounts(models.Model):
    percentage = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transactions(models.Model):
    total = models.IntegerField()
    type = models.CharField(max_length=255)
    transport_fee = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discounts, on_delete=models.CASCADE)
