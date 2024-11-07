from django.shortcuts import render
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.views import api_response, get_error_message
from shop.models import SellerShop, Shop, InvitationCode
from shop.serializers import ShopSerializer, ShopProfileSerializer, InvitationCodeSerializer


class ShopCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        if not request.user.is_authenticated:
            return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)
        if request.user.role != 'SELLER':
            return api_response(False, code=400, message='用户不是卖家', status_code=status.HTTP_403_FORBIDDEN)

        if SellerShop.objects.filter(seller=request.user).exists():
            return api_response(False, code=300, message='用户已经拥有商店', status_code=status.HTTP_403_FORBIDDEN)

        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save()
            SellerShop.objects.create(shop=shop, seller=request.user)
            return api_response(True, code=0)
        else:
            return api_response(False, code=1, message='商铺创建失败', data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class ShopInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        # if not request.user.is_authenticated:
        #     return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            shop = Shop.objects.get(id=id)
            # print(shop)
            serializer = ShopProfileSerializer(shop)
            return api_response(True, code=0, data=serializer.data)
        except Shop.DoesNotExist:
            return api_response(False, code=300, message='商店不存在')


class CreateInvitationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return api_response(False, code=401, message='用户未登录')
        try:
            shop = Shop.objects.get(id=id)
            # 检查用户是否是该商铺的管理者
            if not SellerShop.objects.filter(shop=shop, seller=user).exists():
                return api_response(False, code=301, message='您不是该商铺的管理者')

            serializer = InvitationCodeSerializer(data=request.data, context={'request': request, 'shop': shop})
            if serializer.is_valid():
                serializer.save()
                return api_response(True, code=0, message='邀请码生成成功', data=serializer.data)
            else:
                return api_response(False, code=300, message=get_error_message(serializer.errors), data=serializer.errors)
        except Shop.DoesNotExist:
            return api_response(False, code=1, message='商铺不存在')


class JoinShopByCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        code = request.data.get('invitation_code')
        if not code or len(code) == 0:
            return api_response(False, code=302, message='邀请码不能为空')

        if not user.is_authenticated:
            return api_response(False, code=401, message='用户未登录')

        if user.role != 'SELLER':
            return api_response(False, code=400, message='用户不是卖家')

        try:
            invitation_code = InvitationCode.objects.get(code=code)

            if invitation_code.expires_at and invitation_code.expires_at < timezone.now():
                invitation_code.is_active = False
                invitation_code.save()
                return api_response(False, code=302, message='邀请码已过期')

            if invitation_code.usage_limit and invitation_code.usage_count >= invitation_code.usage_limit:
                invitation_code.is_active = False
                invitation_code.save()
                return api_response(False, code=302, message='邀请码已达到使用次数限制')

            shops = SellerShop.objects.filter(seller=user)
            # 检查用户是否已有商店
            if shops.exists():
                return api_response(False, code=1, message='同一商家只能管理一个商铺')

            invitation_code.usage_count += 1
            if invitation_code.usage_limit and invitation_code.usage_count >= invitation_code.usage_limit:
                invitation_code.is_active = False

            shop = invitation_code.shop
            SellerShop.objects.create(shop=shop, seller=user)

            invitation_code.save()
            return api_response(True, code=0, message='加入商铺成功')

        except InvitationCode.DoesNotExist:
            return api_response(False, code=302, message='邀请码不存在')


class AllShopView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopProfileSerializer(shops, many=True)
        return api_response(True, message='查询所有商铺成功', data=serializer.data)
