from django.db import models

from django.db import models
from django.conf import settings
from shop.models import Product, Shop


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending Payment', '待支付'),
        ('Payment Received', '已支付待收货'),
        ('Completed', '已完成'),
        ('Refund Requested', '申请退款中'),
        ('Refund Successful', '退款成功'),
        ('Cancelled', '已取消'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    # total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Payment')
    recipient_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return f"订单 {self.order_id} - 用户 {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"订单项 {self.id} from 订单 {self.order.id} - 商品 {self.product.name}"
