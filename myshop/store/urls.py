from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product_list, name='product_list'),
    path('/product/<int:product_id>',views.product_detail,name='product_detail'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout,name='checkout'),
]
