from datetime import timedelta

from django.db.models import Avg
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from order.models import OrderItem
from .models import Shop, SellerShop, InvitationCode, Product, Category, ShopTransaction, Review

from accounts.models import User


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ['name', 'address', 'description', 'create_date']


class ShopProfileSerializer(serializers.ModelSerializer):
    sellers = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        avg = Review.objects.filter(product__shop=obj).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None

    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'description', 'create_date', 'sellers', 'total_income', 'average_rating']
        read_only_fields = ['id', 'create_date', 'sellers', 'total_income', 'average_rating']

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


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    # 前端传分类的id
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None

    class Meta:
        model = Product
        fields = [
            'id',
            'shop',
            'name',
            'description',
            'price',
            'stock_quantity',
            'category',
            'status',
            'create_date',
            'image',
            'category_name',
            'average_rating',
            'sales_volume'
        ]
        read_only_fields = ['id', 'shop', 'create_date', 'average_rating', 'sales_volume']
        
    def create(self, validated_data):
        validated_data['shop'] = self.context['shop']
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ShopTransactionSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)

    class Meta:
        model = ShopTransaction
        fields = [
            'id',
            'shop',
            'shop_name',
            'order',
            'order_id',
            'amount',
            'transaction_type',
            'date',
            'description',
        ]
        read_only_fields = ['id', 'shop', 'shop_name', 'order', 'order_id', 'date']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'create_date', 'merchant_reply', 'reply_date']
        read_only_fields = ['id', 'user', 'create_date', 'merchant_reply', 'reply_date']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError({"error": "评分必须在1到5之间"})
        return value

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']

        # 检查用户是否购买过该商品
        purchased_items = OrderItem.objects.filter(
            order__user=user,
            product=product,
            order__status='Completed',
            is_cancelled=False
        )
        if not purchased_items.exists():
            raise serializers.ValidationError("您尚未购买该商品，无法评价")

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("您已评价过该商品，无法重复评价")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['merchant_reply']
        read_only_fields = []

    def validate(self, data):
        request = self.context['request']
        user = request.user
        review = self.instance

        if not SellerShop.objects.filter(seller=user, shop=review.product.shop).exists():
            raise serializers.ValidationError("您无权回复该评价")

        if review.merchant_reply:
            raise serializers.ValidationError("该评价已回复，无法重复回复")

        return data

    def update(self, instance, validated_data):
        instance.merchant_reply = validated_data.get('merchant_reply')
        instance.reply_date = timezone.now()
        instance.save()
        return instance


class ReviewListSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'product',
            'rating',
            'comment',
            'create_date',
            'merchant_reply',
            'reply_date',
        ]
        read_only_fields = fields

