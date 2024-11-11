from rest_framework import serializers
from .models import ShoppingCart, CartItem
from shop.models import Product
from shop.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'updated_time']
        read_only_fields = ['id', 'updated_time']

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(pk=value)
            if product.status != 'Available':
                raise serializers.ValidationError('商品不可用')
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

    def create(self, validated_data):
        cart = self.context['cart']
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': validated_data.get('quantity', 1)}
        )
        if not created:
            cart_item.quantity += validated_data.get('quantity', 1)
            cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'updated_date', 'items']
        read_only_fields = ['id', 'user', 'updated_date', 'items']
