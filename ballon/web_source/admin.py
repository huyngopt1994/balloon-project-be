from django.contrib import admin
from .models import Companies, TransactionProducts, Products, Transactions

admin.site.register(Companies)
admin.site.register(TransactionProducts)
admin.site.register(Products)
admin.site.register(Transactions)
