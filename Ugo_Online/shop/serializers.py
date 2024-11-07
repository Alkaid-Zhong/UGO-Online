from rest_framework import serializers
from .models import Shop, SellerShop
from accounts.serializers import ProfileSerializer
from accounts.models import User


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ['name', 'address', 'description', 'create_date']


class ShopProfileSerializer(serializers.ModelSerializer):
    sellers = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'description', 'create_date', 'sellers']
        read_only_fields = ['id', 'create_date', 'sellers']

    def get_sellers(self, obj):
        seller_shops = SellerShop.objects.filter(shop=obj)
        sellers = [seller_shop.seller for seller_shop in seller_shops]
        return ProfileSerializer(sellers, many=True).data
