from django.db import models
from django.conf import settings
from shop.models import Product
from accounts.models import User


class ShoppingCart(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='cart')
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} 的购物车"


class CartItem(models.Model):
    cart = models.ForeignKey('cart.ShoppingCart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity} in {self.cart}"

