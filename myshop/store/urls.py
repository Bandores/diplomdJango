from django.urls import path
from cart.views import add_to_cart,remove_from_cart,view_cart,increase_cart_item,decrease_cart_item,fetch_cart_count
from .views import product_detail,product_list,index

app_name = 'store'  # Добавьте эту строку
urlpatterns = [
    path('', index, name='index'),
    path('product/', product_list, name='product_list'),
    path('product/<int:product_id>', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', fetch_cart_count, name='fetch-cart-count'),
]
