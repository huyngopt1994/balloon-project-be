from django.contrib import admin
from .models import Users, Discounts, Products, Transactions

admin.site.register(Users)
admin.site.register(Discounts)
admin.site.register(Products)
admin.site.register(Transactions)
