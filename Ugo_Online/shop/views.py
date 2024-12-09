from django.db.models import Avg
from django.shortcuts import render
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.models import User
from accounts.permissions import IsSeller, IsCustomer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from accounts.serializers import ProfileSerializer
from order.models import OrderItem
from shop.filters import ShopTransactionFilter
from shop.pagination import SmallResultsSetPagination
from utils import get_error_message, new_message
from Ugo_Online.utils import api_response, list_response
from shop.models import SellerShop, Shop, InvitationCode, Product, Category, ShopTransaction, Review
from shop.serializers import ShopSerializer, ShopProfileSerializer, InvitationCodeSerializer, ProductSerializer, \
    CategorySerializer, ShopTransactionSerializer, ReviewReplySerializer, ReviewSerializer, ReviewListSerializer


class ShopCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request):

        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.save()
            SellerShop.objects.create(shop=shop, seller=request.user)
            serializer2 = ShopSerializer(shop)
            return api_response(True, code=0, data=serializer2.data)
        else:
            return api_response(False, code=1, message='商铺创建失败', data=serializer.errors,
                                status_code=status.HTTP_400_BAD_REQUEST)


class ShopInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):

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

            # shops = SellerShop.objects.filter(seller=user)
            # # 检查用户是否已有商店
            # if shops.exists():
            #     return api_response(False, code=300, message='同一商家只能管理一个商铺')

            invitation_code.usage_count += 1
            if invitation_code.usage_limit and invitation_code.usage_count >= invitation_code.usage_limit:
                invitation_code.is_active = False

            shop = invitation_code.shop

            sellers = shop.sellers.all()
            for seller in sellers:
                new_message(seller, f"[{shop}] 用户 {user} 加入了您的商店。", -1, shop.id)

            SellerShop.objects.create(shop=shop, seller=user)

            invitation_code.save()

            serializer = ShopSerializer(shop)
            return api_response(True, code=0, message='加入商铺成功', data=serializer.data)

        except InvitationCode.DoesNotExist:
            return api_response(False, code=302, message='邀请码不存在')


class ShopListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShopProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    search_fields = ['name', 'description', 'address']
    ordering_fields = ['average_rating', 'name', 'create_date']
    ordering = ['-average_rating']  # 默认按照平均评分降序排列

    def get_queryset(self):
        return Shop.objects.all().annotate(
            average_rating=Avg('products__reviews__rating')
        )

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

    def put(self, request, id):
        user = request.user
        try:
            shop = Shop.objects.get(id=id)
        except Shop.DoesNotExist:
            return api_response(False, code=300, message='商铺不存在')
        try:
            product = Product.objects.get(id=request.data['product_id'])
        except Product.DoesNotExist:
            return api_response(False, code=300, message='商品不存在')

        if not SellerShop.objects.filter(seller=user, shop=shop).exists():
            return api_response(False, code=301, message='您不是该商铺的管理者')
        serializer = ProductSerializer(product, data=request.data, context={'shop': shop}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, code=0, message='商品修改成功', data=serializer.data)
        else:
            return api_response(False, code=300, message=get_error_message(serializer.errors), data=serializer.errors)

    def delete(self, request, id):

        user = request.user
        try:
            shop = Shop.objects.get(id=id)
        except Shop.DoesNotExist:
            return api_response(False, code=300, message='商铺不存在')
        try:
            product = Product.objects.get(id=request.data['product_id'])
        except Product.DoesNotExist:
            return api_response(False, code=300, message='商品不存在')
        if not SellerShop.objects.filter(seller=user, shop=shop).exists():
            return api_response(False, code=301, message='您不是该商铺的管理者')
        product.status = 'Unavailable'
        product.save()
        return api_response(True, code=0, message='商品删除成功')


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'price': ['gte', 'lte'],
        'status': ['exact'],
        'stock_quantity': ['exact']
    }
    search_fields = ['name', 'description', 'shop__name']
    ordering_fields = ['average_rating', 'name', 'create_date', 'price', 'sales_volume']
    ordering = ['-average_rating']  # 默认按照平均评分降序排列

    shop = None

    # show_all = False

    def get_queryset(self):
        if self.shop is not None:
            if self.request.user.is_authenticated and SellerShop.objects.filter(seller=self.request.user, shop=self.shop).exists():
                queryset = Product.objects.filter(shop=self.shop)
            else:
                queryset = Product.objects.filter(shop=self.shop, status='Available', stock_quantity__gt=0)
        else:
            queryset = Product.objects.filter(status='Available', stock_quantity__gt=0)
        return queryset.annotate(
            average_rating=Avg('reviews__rating')
        )

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

    filter_backends = [OrderingFilter]
    ordering_fields = ['id']
    ordering = ['id']

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

        query_set = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(query_set, many=True)
        return api_response(True, code=0, data={'categories': serializer.data})


class ShopTransactionListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSeller]
    serializer_class = ShopTransactionSerializer
    filterset_class = ShopTransactionFilter
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
        order_id = request.data.get('order')

        try:
            order = OrderItem.objects.get(id=order_id)
        except OrderItem.DoesNotExist:
            return api_response(False, code=404, message='订单不存在')

        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            sellers = order.product.shop.sellers.all()
            for seller in sellers:
                new_message(seller, f"[{order.product.shop}] 您的商品 {order.product} 有新的评价，快去看看吧！", order.id, order.product.shop.id)

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
            new_message(review.user, f"[{review.product.shop}] 您对商品 {review.product} 的评价已被商家回复，快去看看吧！", review.order.id, review.product.shop.id)
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
    pagination_class = SmallResultsSetPagination    # 可选，添加分页功能

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


class OrderItemReviewView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get(self, request, order_item_id):
        try:
            OrderItem.objects.get(id=order_item_id)
        except OrderItem.DoesNotExist:
            return api_response(False, code=404, message='订单项不存在')

        try:
            review = Review.objects.get(order__id=order_item_id)
            serializer = ReviewSerializer(review, context={'request': request})
            return api_response(True, data=serializer.data)
        except Review.DoesNotExist:
            return api_response(False, code=404, message='评论不存在')


class ShopOwnersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, shop_id):
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            return api_response(False, code=404, message='店铺不存在')
        shop_owners = shop.sellers.all()

        serializer = ProfileSerializer(shop_owners, many=True, context={'request': request})
        return api_response(True, data=serializer.data)


# 商店分成
class ShopCommissionView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request, shop_id):
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            return api_response(False, code=404, message='店铺不存在')

        getter_id = request.data.get("given_id")

        try :
            getter = User.objects.get(id=getter_id)
        except User.DoesNotExist:
            return api_response(False, code=404, message='用户不存在')

        money = request.data.get("money")
        if shop.total_income < money:
            return api_response(False, code=404, message='店铺余额不足')
        shop.total_income -= money
        shop.save()
        getter.money += money
        getter.save()

        ShopTransaction.objects.create(
            shop=shop,
            order=None,
            amount=-money,
            transaction_type='Divide',
            description=f"Divided {money} to {getter}"
        )

        new_message(getter, f'[{shop}] 您得到了 {money} 元的分成！', -1, shop.id)

        return api_response(True, message='分成成功')

