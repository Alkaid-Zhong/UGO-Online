from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ['name', 'address', 'description', 'create_date']


class ShopProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'description', 'create_date']


