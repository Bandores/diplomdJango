from django.db.models import Q
from django.core.files.base import ContentFile
from django.shortcuts import render,redirect
from .models import Category, Product
from .utils import resize_image
from .models import Product, Cart, CartItem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse



def index(request):
    return render(request, 'store/index.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    # Загрузка изображения по URL и сохранение в поле ImageField
    return render(request, 'store/product_detail.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    category = Category.objects.all()
    query = request.GET.get('q')
    
    if query:
        # Используем Q-объекты для поиска в нескольких полях модели
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    # Остальная часть вашей функции остается неизменной
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_id = request.GET.get('category')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Остальной код

    return render(request, 'store/product_list.html', {'products': products, 'category': category, 'query': query})




