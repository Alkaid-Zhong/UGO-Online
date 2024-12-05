from collections import defaultdict

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics
from django.db import transaction

from Ugo_Online.utils import list_response
from accounts.models import Address
from shop.models import Shop, SellerShop, ShopTransaction
from utils import get_error_message, new_message
from .models import Order
from .serializers import OrderSerializer, PaymentSerializer, UpdateOrderAddressSerializer
from accounts.views import api_response
from accounts.permissions import IsSeller, IsCustomer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return api_response(True, message='订单创建成功', data=serializer.data)
        else:
            return api_response(False, code=201, message=get_error_message(serializer.errors), data=serializer.errors)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['order_date']
    ordering = ['-order_date']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return list_response(paginated_response, self.paginator, 'orders')
        else:
            serializer = self.get_serializer(queryset, many=True)
            return api_response(True, code=0, data={'orders': serializer.data})


class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['order_date']
    ordering = ['-order_date']

    shop = None

    def get_queryset(self):
        return Order.objects.filter(shop=self.shop)

    def list(self, request, *args, **kwargs):

        user = request.user
        shop_id = self.kwargs.get('shop_id')
        try:
            self.shop = Shop.objects.get(id=shop_id)
            SellerShop.objects.get(shop=self.shop, seller=user)
        except SellerShop.DoesNotExist or Shop.DoesNotExist:
            return api_response(False, code=201, message='您未拥有该商铺的管理权限')

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return list_response(paginated_response, self.paginator, 'orders')
        else:
            serializer = self.get_serializer(queryset, many=True)
            return api_response(True, code=0, data={'orders': serializer.data})


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return api_response(False, code=201, message='订单不存在')
        if order.user != request.user and SellerShop.objects.filter(shop=order.shop, seller=request.user).count() == 0:
            return api_response(False, code=201, message='您无权查看该订单')
        serializer = OrderSerializer(order)
        return api_response(True, code=0, data=serializer.data)


class OrderPaymentView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            order_ids = serializer.validated_data['order_ids']
            orders = Order.objects.filter(id__in=order_ids, user=request.user, status='Pending Payment')

            if orders.count() != len(order_ids):
                return api_response(False, code=201, message='部分订单不存在或不可支付')

            total_amount = sum(order.total_price for order in orders)

            if request.user.money < total_amount:
                return api_response(False, code=201, message='余额不足')

            # 扣除用户余额
            request.user.money -= total_amount
            request.user.save()

            for order in orders:
                shop = order.shop
                shop.total_income += order.total_price
                shop.save()

                ShopTransaction.objects.create(
                    shop=shop,
                    order=order,
                    amount=order.total_price,
                    transaction_type='Income',
                    description=f"Payment for {order}"
                )

                sellers = shop.sellers.all()

                for seller in sellers:
                    new_message(seller, f'[{order.shop.name}] 用户 {order.user} 已支付订单 {order.id}，请尽快发货！')

            # 更新订单状态
            orders.update(status='Payment Received')

            return api_response(True, message='支付成功')
        else:
            return api_response(False, code=201, message=get_error_message(serializer.errors))


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return api_response(False, code=404, message='订单不存在')

        if order.status != 'Pending Payment':
            return api_response(False, code=400, message=f'订单{order.get_status_display()}，不可取消')

        # 恢复商品库存
        for item in order.items.all():
            product = item.product
            product.stock_quantity += item.quantity
            product.sales_volume -= item.quantity
            product.save()

        order.status = 'Cancelled'
        order.save()

        sellers = order.shop.sellers.all()

        for seller in sellers:
            new_message(seller, f'[{order.shop.name}] 用户 {order.user} 取消了订单 {order.id}！')

        return api_response(True, message='订单已取消')


class RefundOrderItemsView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, order_id):
        item_ids = request.data.get('item_ids', [])
        # order_id = request.data.get('order_id')
        if not item_ids:
            return api_response(False, code=201, message='未提供商品项ID')

        if not order_id:
            return api_response(False, code=201, message='未提供订单ID')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return api_response(False, code=404, message='订单不存在')

        if order.status != 'Payment Received':
            return api_response(False, code=201, message=f'订单{order.get_status_display()}，不支持退款')

        order_items = order.items.filter(id__in=item_ids)

        if order_items.count() != len(item_ids):
            return api_response(False, code=201, message='部分商品项不存在')

        sellers = order.shop.sellers.all()

        total_refund = 0
        for item in order_items:
            if item.is_cancelled:
                return api_response(False, code=201, message=f'商品项{item.id}不可重复退款')

        for item in order_items:
            item.is_cancelled = True
            item.save()

            # 恢复商品库存
            product = item.product
            product.stock_quantity += item.quantity
            product.sales_volume -= item.quantity
            product.save()

            for seller in sellers:
                new_message(seller, f'[{order.shop.name}] 用户 {order.user} 退回了订单 {order.id} 中的商品项 {item.product}！')

            total_refund += item.total_price

        request.user.money += total_refund
        request.user.save()

        ShopTransaction.objects.create(
            shop=order.shop,
            order=order,
            amount=-total_refund,  # Refund amount is negative
            transaction_type='Refund',
            description=f"Refund for Order {order}, Items: {', '.join(map(str, item_ids))}"
        )

        order.shop.total_income -= total_refund
        order.shop.save()

        order.total_price -= total_refund
        order.save()

        if order.items.filter(is_cancelled=False).count() == 0:
            assert order.total_price == 0
            order.status = 'Cancelled'
            order.save()

        return api_response(True, message='退款成功')


class UpdateOrderStatus2ShippedView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return api_response(False, code=404, message='订单不存在')

        if not SellerShop.objects.filter(seller=request.user, shop=order.shop).exists():
            return api_response(False, code=403, message='您无权操作该订单')

        if order.status != 'Payment Received':
            return api_response(False, code=201, message=f'订单{order.get_status_display()}，不可更新为已发货')

        order.status = 'Shipped'
        order.save()

        new_message(order.user, f'您的订单 {order.id} 已发货，请在收到货后确认收货！')

        return api_response(True, message='订单状态已更新为已发货')


class UpdateOrderStatus2CompletedView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return api_response(False, code=404, message='订单不存在')

        if order.user != request.user:
            return api_response(False, code=403, message='您无权操作该订单')

        if order.status != 'Shipped':
            return api_response(False, code=201, message=f'订单{order.get_status_display()}，不可更新为已完成')

        order.status = 'Completed'
        order.save()
        return api_response(True, message='订单状态已更新为已完成')


class UpdateOrderAddressView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, order_id):
        # 获取订单
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return api_response(False, code=404, message='订单不存在或不属于当前用户')

        if order.status not in ['Pending Payment', 'Payment Received']:
            return api_response(False, code=400, message=f'订单{order.get_status_display()}，不允许修改地址')

        serializer = UpdateOrderAddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            address_id = serializer.validated_data['address_id']
            address = Address.objects.get(id=address_id)

            order.recipient_name = address.recipient_name
            order.address = address.address
            order.city = address.city
            order.province = address.province
            order.phone = address.phone
            order.save()

            sellers = order.shop.sellers.all()
            for seller in sellers:
                new_message(seller, f'[{order.shop}] 订单 {order.id} 的地址已修改为 "{address}"！')

            return api_response(True, message='订单地址修改成功')
        else:
            return api_response(False, code=400, message=get_error_message(serializer.errors), data=serializer.errors)

