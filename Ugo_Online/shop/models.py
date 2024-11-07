from django.db import models


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

