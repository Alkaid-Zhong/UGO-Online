from django.contrib import admin

from shop.models import Shop, SellerShop, InvitationCode, Category, Product, Review, ShopTransaction

# Register your models here.

admin.site.register(Shop)
admin.site.register(SellerShop)
admin.site.register(InvitationCode)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ShopTransaction)
