from django.contrib import admin
from shop.models import Category, Product, Comment, Order

# Register your models here.

admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Comment)

admin.site.register(Order)