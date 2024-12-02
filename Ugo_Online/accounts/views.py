from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsSeller
from django.contrib.auth import login, logout

from Ugo_Online.utils import api_response
from order.models import Order
from order.serializers import OrderSerializer
from utils import get_error_message, new_message
from .permissions import IsCustomer
from .models import Address
from .serializers import (
    UserRegistrationSerializer,
    MerchantRegistrationSerializer,
    LoginSerializer,
    ProfileSerializer, ChangePasswordSerializer, AddressSerializer, AddMoneySerializer
)

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, message='注册成功')
        else:
            return api_response(False, code=402, message=get_error_message(serializer.errors), data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class SellerRegistrationView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        serializer = MerchantRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, message='注册成功')
        else:
            return api_response(False, code=402, message=get_error_message(serializer.errors), data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return api_response(True, message='登录成功')
        else:
            error = serializer.errors
            return api_response(False, code=403, message=get_error_message(serializer.errors), data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request):

        # if not request.user.is_authenticated:
        #     return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        logout(request)
        return api_response(True, message='登出成功')


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def get(self, request):

        # if not request.user.is_authenticated:
        #     return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        serializer = ProfileSerializer(request.user)
        return api_response(True, data=serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # if not request.user.is_authenticated:
        #     return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.update_password()
            login(request, user)
            return api_response(True, code=0)
        else:
            return api_response(False, code=403, message=get_error_message(serializer.errors), data=serializer.errors, status_code=status.HTTP_403_FORBIDDEN)


class AddressCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return api_response(True, message='地址创建成功', data=serializer.data)
        else:
            return api_response(False, code=500, message=get_error_message(serializer.errors), data=serializer.errors)


class AddressListView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        # 让默认地址在list的第一个
        addresses = Address.objects.filter(user=request.user)
        addresses = sorted(addresses, key=lambda x: x.is_default, reverse=True)
        serializer = AddressSerializer(addresses, many=True)
        return api_response(True, data=serializer.data)


class DefaultAddressView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        try:
            address = Address.objects.get(user=request.user, is_default=True)
            serializer = AddressSerializer(address)
            return api_response(True, data=serializer.data)
        except Address.DoesNotExist:
            return api_response(True, data=None)


class AddressDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(user=request.user, id=address_id)
            # address.delete()
            # 软删除
            address.user = None
            return api_response(True, message='地址删除成功')
        except Address.DoesNotExist:
            return api_response(False, code=404, message='地址不存在')


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, address_id):
        try:
            address = Address.objects.get(user=request.user, id=address_id)
            serializer = AddressSerializer(address)
            return api_response(True, data=serializer.data)
        except Address.DoesNotExist:
            return api_response(False, code=404, message='地址不存在')


class AddressUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def put(self, request, address_id):
        try:
            address = Address.objects.get(user=request.user, id=address_id)
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return api_response(True, message='地址更新成功', data=serializer.data)
            else:
                return api_response(False, code=500, message=get_error_message(serializer.errors), data=serializer.errors)
        except Address.DoesNotExist:
            return api_response(False, code=404, message='地址不存在')


class AddMoneyView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        serializer = AddMoneySerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_message(request.user, "充值成功，账户当前余额为 " + str(request.user.money) + " 元。")
            return api_response(True, message='充值成功', data=serializer.data)
        else:
            return api_response(False, code=500, message=get_error_message(serializer.errors), data=serializer.errors)
