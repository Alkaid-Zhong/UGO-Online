from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Ugo_Online.utils import api_response
from accounts.permissions import IsCustomer, IsSeller
from shop.models import Product
from utils import get_error_message
from .models import ShoppingCart, CartItem
from .serializers import CartItemSerializer


class CartItemView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):

        user = request.user
        cart, created = ShoppingCart.objects.get_or_create(user=user)

        serializer = CartItemSerializer(data=request.data, context={'cart': cart})

        if serializer.is_valid():
            serializer.save()
            return api_response(True, code=0, message='加入购物车成功', data=serializer.data)
        else:
            return api_response(False, code=200, message=get_error_message(serializer.errors), data=serializer.errors)

    def put(self, request):
        user = request.user
        item_id = request.data.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=user)

        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)  # 可以只改部分

        if serializer.is_valid():
            if 'quantity' in serializer.validated_data and serializer.validated_data['quantity'] <= 0:
                cart_item.delete()
                return api_response(True, code=0, message='商品已成功从购物车移除', data=serializer.data)
            serializer.save()
            return api_response(True, code=0, message='购物车已更新', data=serializer.data)
        else:
            return api_response(False, code=200, message=get_error_message(serializer.errors), data=serializer.errors)

    def delete(self, request):
        user = request.user
        item_id = request.data.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=user)

        cart_item.delete()
        return api_response(True, code=0, message='商品已成功从购物车移除')


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        user = request.user
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_items = cart.items.select_related('product__shop')

        # 按商店分类商品
        shop_dict = {}
        for item in cart_items:
            shop = item.product.shop
            if shop.id not in shop_dict:
                shop_dict[shop.id] = {
                    'shop_id': shop.id,
                    'shop_name': shop.name,
                    'items': []
                }
            shop_dict[shop.id]['items'].append({
                'item_id': item.id,
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': str(item.product.price),
                'total_price': str(item.product.price * item.quantity),
                'image': request.build_absolute_uri(item.product.image.url) if item.product.image else None
            })

        data = list(shop_dict.values())
        return api_response(True, data={'shops': data})
