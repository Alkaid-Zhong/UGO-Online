from django.contrib import admin

from shop.models import Shop, SellerShop, InvitationCode, Category, Product

# Register your models here.

admin.site.register(Shop)
admin.site.register(SellerShop)
admin.site.register(InvitationCode)
admin.site.register(Category)
admin.site.register(Product)
