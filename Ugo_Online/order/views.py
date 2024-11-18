from collections import defaultdict

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics
from django.db import transaction

from Ugo_Online.utils import list_response
from utils import get_error_message
from .models import Order
from .serializers import OrderSerializer
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

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



