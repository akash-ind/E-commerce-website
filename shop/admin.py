from django.contrib import admin
from .models import Product, ProductCategory, ProductWithCount, Cart, Order, CustomOrder
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductWithCount)
admin.site.register(Order)
admin.site.register(CustomOrder)
admin.site.register(Cart)