from django.contrib import admin
from .models import Category, Product,Cart, CartItem
app_name = 'store'

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
