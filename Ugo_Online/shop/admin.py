from django.contrib import admin

from shop.models import Shop, SellerShop, InvitationCode

# Register your models here.

admin.site.register(Shop)
admin.site.register(SellerShop)
admin.site.register(InvitationCode)
