from django.contrib import admin
from .models import Category, Product,Cart, CartItem,Purchase
app_name = 'store'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Поля для отображения в таблице

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category_name', 'price', 'img', 'total']  # Поля для отображения в таблице
    list_filter = ['category']  # Добавление фильтрации по категории

    def category_name(self, obj):
        return obj.category.name

    category_name.short_description = 'Категория'

admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Purchase)