from django.shortcuts import render
from store.models import Category, Product,Cart, CartItem
from collections import Counter
from itertools import groupby
from operator import attrgetter
from django.core.files.base import ContentFile
from django.shortcuts import render,redirect
from store.models import Category, Product,Purchase
from store.utils import resize_image
from store.models import Product, Cart, CartItem
from django.http import HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
# Create your views here.
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from .forms import OrderForm
from django.shortcuts import get_object_or_404

@login_required(login_url='users:login')
def buy_single_product(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        cart = request.user.cart
        cart_item = cart.cartitem_set.get(product=product)
        form = OrderForm(request.POST)
        
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            city = form.cleaned_data['city']
            phone = form.cleaned_data['phone']

            if cart_item.quantity > 0:
                with transaction.atomic():
                    # Уменьшаем количество продукта (total) на количество, которое покупается
                    product.total -= cart_item.quantity
                    product.save()

                    # Создаем заказ
                    Purchase.objects.create(user=request.user, product=product, full_name=full_name, city=city, phone=phone)

                    # Уменьшаем количество товара в корзине
                    cart_item.quantity -= 1
                    cart_item.save()

                messages.success(request, 'Продукт успешно куплен!')
            else:
                messages.error(request, 'Продукт закончился на складе!')

            return redirect('store:cart')
    else:
        form = OrderForm()

    return render(request, 'store/order_form.html', {'form': form})
@login_required(login_url='users:login')
def user_orders(request):
    # Получаем все заказы текущего пользователя
    orders = Purchase.objects.filter(user=request.user).order_by('created_at')
    
    # Создаем словарь, где ключами будут даты создания заказов,
    # а значениями будут списки заказов, сделанных в эту дату
    grouped_orders = {}
    for order in orders:
        created_at = order.created_at.date()
        if created_at not in grouped_orders:
            grouped_orders[created_at] = []
        grouped_orders[created_at].append(order)

    # Обработка повторяющихся продуктов
    for created_at, orders in grouped_orders.items():
        product_counter = Counter(order.product for order in orders)
        grouped_orders[created_at] = [(product, count) for product, count in product_counter.items()]

    return render(request, 'store/user_orders.html', {'grouped_orders': grouped_orders})
@login_required(login_url='users:login')
def buy_all_products(request):
    if request.method == 'POST':
        cart = request.user.cart
        cart_items = cart.cartitem_set.all()
        form = OrderForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            city = form.cleaned_data['city']
            phone = form.cleaned_data['phone']

            with transaction.atomic():
                for cart_item in cart_items:
                    if cart_item.quantity > 0:
                        product = cart_item.product
                        product.total -= cart_item.quantity
                        product.save()

                        for _ in range(cart_item.quantity):
                            # Создаем заказ для каждого товара в корзине
                            Purchase.objects.create(user=request.user, product=product, full_name=full_name, city=city, phone=phone)

                        cart_item.quantity = 0
                        cart_item.save()

                messages.success(request, 'Все продукты успешно куплены!')

            return redirect('store:cart')
    else:
        form = OrderForm()

    return render(request, 'store/order_form.html', {'form': form})
@require_POST
@login_required(login_url='/users/login/')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        
        return HttpResponseRedirect(reverse('store:cart'))
    else:
        # Если метод запроса не POST, например, GET,
        # вы можете вернуть другой HTTP-ответ, например, 405 Method Not Allowed.
        return HttpResponseNotAllowed(['POST'])
@login_required(login_url='users:login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('store:cart')
@login_required(login_url='users:login')
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='users:login')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('store:cart')

@login_required(login_url='users:login')
def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('store:cart')

@login_required(login_url='users:login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count