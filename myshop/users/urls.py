from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # Используется ваше представление
    path('login/', auth_views.LoginView.as_view(), name='login_default'),  # Используется встроенное представление
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]