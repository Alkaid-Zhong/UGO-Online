from datetime import timedelta

from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import Shop, SellerShop, InvitationCode

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
        from accounts.serializers import ProfileSerializer
        seller_shops = SellerShop.objects.filter(shop=obj)
        sellers = [seller_shop.seller for seller_shop in seller_shops]
        return ProfileSerializer(sellers, many=True).data

class InvitationCodeSerializer(serializers.ModelSerializer):

    expires_in_days = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = InvitationCode
        fields = ['code', 'shop', 'creator', 'is_active', 'created_at', 'expires_at', 'usage_limit', 'usage_count', 'expires_in_days']
        read_only_fields = ['code', 'shop', 'creator', 'is_active', 'created_at', 'usage_count']

    def create(self, validated_data):
        expires_in_days = validated_data.pop('expires_in_days', None)
        validated_data['code'] = self.generate_code()
        validated_data['creator'] = self.context['request'].user
        validated_data['shop'] = self.context['shop']
        if expires_in_days is not None:
            validated_data['expires_at'] = timezone.now() + timedelta(days=expires_in_days)
        return super().create(validated_data)

    def generate_code(self):
        while True:
            code = get_random_string(length=16)
            if not InvitationCode.objects.filter(code=code).exists():
                return code
