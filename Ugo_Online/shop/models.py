from django.db import models

from accounts.models import User


class Shop(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class SellerShop(models.Model):
    seller = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='seller_shops')
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='shop_sellers')

    class Meta:
        unique_together = ('seller', 'shop')

    def __str__(self):
        return f'{self.seller.email} - {self.shop.name}'


class InvitationCode(models.Model):
    code = models.CharField(max_length=16, unique=True)  # 邀请码
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='invitation_codes')
    creator = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_invitation_codes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # 可选：邀请码过期时间
    usage_limit = models.IntegerField(default=1)  # 可选：使用次数限制
    usage_count = models.IntegerField(default=0)  # 已使用次数

    def __str__(self):
        return f"{self.code} for {self.shop.name}"


class Product(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    )

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stock_quantity = models.IntegerField(default=0, null=False)
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products', default=11)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Available')
    create_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # 销量
    sales_volume = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class ShopTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('Income', 'Income'),
        ('Refund', 'Refund'),
    )

    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for {self.shop.name} on {self.date}"


class Review(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('order.OrderItem', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    merchant_reply = models.TextField(blank=True, null=True)
    reply_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'order')

    def __str__(self):
        return f"Review of {self.product.name} by {self.user.name}"
