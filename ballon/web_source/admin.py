from django.contrib import admin
from .models import Companies, Discounts, Products, Transactions

admin.site.register(Companies)
admin.site.register(Discounts)
admin.site.register(Products)
admin.site.register(Transactions)
