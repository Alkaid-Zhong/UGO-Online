from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.views import api_response
from shop.models import SellerShop
from shop.serializers import ShopSerializer


class ShopCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        if not request.user.is_authenticated:
            return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)
        if request.user.role != 'SELLER':
            return api_response(False, code=400, message='用户不是卖家', status_code=status.HTTP_403_FORBIDDEN)

        # TODO：判断用户是否没有商店。（一个用户只能管理一个商店，一个商店可以由多个用户管理）

        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save()
            SellerShop.objects.create(shop=shop, seller=request.user)
            return api_response(True, code=0)
        else:
            return api_response(False, code=1, message='商铺创建失败', data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
