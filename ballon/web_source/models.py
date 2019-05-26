from django.db import models


# Create your models here.
class Companies(models.Model):
    name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    tax_number = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    address = models.TextField(default='')
    logo = models.ImageField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Products(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    image = models.ImageField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Discounts(models.Model):
    percentage = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transactions(models.Model):
    NORMAL_TYPE = 'NT'
    RED_TYPE = 'RT'
    TYPE_TRANSACTIONS_CHOICES = [
        (NORMAL_TYPE, 'Normaltype'),
        (RED_TYPE, 'Redtype')

    ]
    total = models.IntegerField()
    type = models.CharField(max_length=2, choices=TYPE_TRANSACTIONS_CHOICES, default=NORMAL_TYPE)
    transport_fee = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=False)
    discount = models.ForeignKey(Discounts, on_delete=models.CASCADE, null=False)
    price = models.IntegerField(default=0)
