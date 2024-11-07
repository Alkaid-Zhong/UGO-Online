from django.db import models

from accounts.models import User


class Shop(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SellerShop(models.Model):
    seller = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='seller_shops')
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='shop_seller')

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
