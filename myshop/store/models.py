from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    img = models.URLField(null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
#
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

User.cart = property(lambda u: Cart.objects.get_or_create(user=u)[0])

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_purchases')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    city = models.CharField(max_length=100, verbose_name='Город')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True)
