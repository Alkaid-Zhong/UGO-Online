from django.db import models


class Shop(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SellerShop(models.Model):
    merchant = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='merchant_shops')
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='shop_merchants')

    class Meta:
        unique_together = ('merchant', 'shop')

    def __str__(self):
        return f'{self.merchant.email} - {self.shop.name}'

