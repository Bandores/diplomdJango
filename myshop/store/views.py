from django.db.models import Q
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from .models import Category, Product
from .utils import resize_image


def index(request):
    return render(request, 'store/index.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    # Загрузка изображения по URL и сохранение в поле ImageField
    if product.image_url:
        response = requests.get(product.image_url)
        product.image.save(f'{product.name}_image.jpg', ContentFile(response.content), save=True)

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

    return render(request, 'your_template.html', {'products': products, 'category': category, 'query': query})
def cart(request):
    # Логика для отображения корзины
    return render(request, 'store/cart.html')

def checkout(request):
    # Логика оформления заказа
    return render(request, 'store/checkout.html')

