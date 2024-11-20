from django.shortcuts import render
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsSeller, IsCustomer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from utils import get_error_message
from Ugo_Online.utils import api_response, list_response
from shop.models import SellerShop, Shop, InvitationCode, Product, Category, ShopTransaction, Review
from shop.serializers import ShopSerializer, ShopProfileSerializer, InvitationCodeSerializer, ProductSerializer, \
    CategorySerializer, ShopTransactionSerializer, ReviewReplySerializer, ReviewSerializer, ReviewListSerializer


class ShopCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):

        # if not request.user.is_authenticated:
        #     return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)
        # if request.user.role != 'SELLER':
        #     return api_response(False, code=400, message='用户不是卖家', status_code=status.HTTP_403_FORBIDDEN)

        if SellerShop.objects.filter(seller=request.user).exists():
            return api_response(False, code=300, message='用户已经拥有商店', status_code=status.HTTP_403_FORBIDDEN)

        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save()
            SellerShop.objects.create(shop=shop, seller=request.user)
            return api_response(True, code=0)
        else:
            return api_response(False, code=1, message='商铺创建失败', data=serializer.errors,
                                status_code=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request, id):
        user = request.user
        # if not user.is_authenticated:
        #     return api_response(False, code=401, message='用户未登录')
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
                return api_response(False, code=300, message=get_error_message(serializer.errors),
                                    data=serializer.errors)
        except Shop.DoesNotExist:
            return api_response(False, code=300, message='商铺不存在')


class JoinShopByCodeView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):
        user = request.user
        code = request.data.get('invitation_code')
        if not code or len(code) == 0:
            return api_response(False, code=302, message='邀请码不能为空')

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
                return api_response(False, code=300, message='同一商家只能管理一个商铺')

            invitation_code.usage_count += 1
            if invitation_code.usage_limit and invitation_code.usage_count >= invitation_code.usage_limit:
                invitation_code.is_active = False

            shop = invitation_code.shop
            SellerShop.objects.create(shop=shop, seller=user)

            invitation_code.save()
            return api_response(True, code=0, message='加入商铺成功')

        except InvitationCode.DoesNotExist:
            return api_response(False, code=302, message='邀请码不存在')


class ShopListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShopProfileSerializer

    def get_queryset(self):
        return Shop.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data

            return list_response(paginated_response, self.paginator, 'shops')
        else:
            serializer = self.get_serializer(queryset, many=True)
            return api_response(True, code=0, data={'shops': serializer.data})


class AddProductView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request, id):
        user = request.user
        try:
            shop = Shop.objects.get(id=id)
        except Shop.DoesNotExist:
            return api_response(False, code=300, message='商铺不存在')

        if not SellerShop.objects.filter(seller=user, shop=shop).exists():
            return api_response(False, code=301, message='您不是该商铺的管理者')

        serializer = ProductSerializer(data=request.data, context={'shop': shop})

        if serializer.is_valid():
            serializer.save()
            return api_response(True, code=0, message='商品创建成功', data=serializer.data)
        else:
            return api_response(False, code=300, message=get_error_message(serializer.errors), data=serializer.errors)


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    shop = None

    def get_queryset(self):
        if self.shop is not None:
            return Product.objects.filter(shop=self.shop, status='Available')
        else:
            return Product.objects.filter(status='Available')

    def list(self, request, *args, **kwargs):
        shop_id = self.kwargs.get('shop_id')
        if shop_id is not None:
            try:
                self.shop = Shop.objects.get(id=shop_id)
            except Shop.DoesNotExist:
                return api_response(False, code=300, message='商铺不存在')
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return list_response(paginated_response, self.paginator, 'products')
        else:
            serializer = self.get_serializer(queryset, many=True)
            return api_response(True, code=0, data={'products': serializer.data})


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    shop = None

    def get_queryset(self):
        if self.shop is not None:
            return Category.objects.filter(products__shop=self.shop).distinct()
        else:
            return super().get_queryset()

    def list(self, request, *args, **kwargs):
        shop_id = self.kwargs.get('shop_id')
        if shop_id is not None:
            try:
                self.shop = Shop.objects.get(id=shop_id)
            except Shop.DoesNotExists:
                api_response(False, code=300, message='商铺不存在')

        query_set = self.get_queryset()
        serializer = self.get_serializer(query_set, many=True)
        return api_response(True, code=0, data={'categories': serializer.data})


class ShopTransactionListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSeller]
    serializer_class = ShopTransactionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['transaction_type', 'date']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']

    shop = None

    def get_queryset(self):

        return ShopTransaction.objects.filter(shop=self.shop)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        shop_id = self.kwargs.get('shop_id')

        try:
            self.shop = SellerShop.objects.get(shop__id=shop_id, seller=user).shop
        except SellerShop.DoesNotExist:
            return api_response(False, code=300, message='商铺不存在或者您不是该商铺的管理者')

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return list_response(paginated_response, self.paginator, 'transactions')
        else:
            serializer = self.get_serializer(queryset, many=True)
            return api_response(True, code=0, data={'transactions': serializer.data})


class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return api_response(True, message='评价提交成功', data=serializer.data)
        else:
            return api_response(False, code=400, message=get_error_message(serializer.errors), data=serializer.errors)


class ReviewReplyView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def put(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return api_response(False, code=404, message='评价不存在')

        serializer = ReviewReplySerializer(review, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return api_response(True, message='回复成功')
        else:
            return api_response(False, code=400, message=get_error_message(serializer.errors), data=serializer.errors)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, context={'request': request})
            return api_response(True, data=serializer.data)
        except Product.DoesNotExist:
            return api_response(False, code=404, message='商品不存在')


class ProductReviewListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewListSerializer
    pagination_class = PageNumberPagination  # 可选，添加分页功能

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product__id=product_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return list_response(paginated_response, self.paginator, 'reviews')
        else:
            serializer = self.get_serializer(queryset, many=True)
            return api_response(True, code=0, data={'reviews': serializer.data})