from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout

from . import serializers
from .serializers import (
    UserRegistrationSerializer,
    MerchantRegistrationSerializer,
    LoginSerializer,
    ProfileSerializer, ChangePasswordSerializer
)
from .models import User


def get_error_message(errors):
    for field, error_list in errors.items():
        if isinstance(error_list, dict):
            return get_error_message(error_list)  # 递归找到第一个错误
        elif isinstance(error_list, list):
            for error in error_list:
                if isinstance(error, dict):
                    return get_error_message(error)  # 如果是嵌套的字典，继续递归
                else:
                    return str(error)  # 直接返回第一个错误信息
        else:
            return str(error_list)




def api_response(success, code=0, message='', data=None, status_code=status.HTTP_200_OK):
    if not success and status_code == status.HTTP_200_OK:
        status_code = status.HTTP_400_BAD_REQUEST
    return Response({
        'success': success,
        'code': code,
        'message': message,
        'data': data
    }, status=status_code)


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
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):

        if not request.user.is_authenticated:
            return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        logout(request)
        return api_response(True, message='登出成功')


class UserProfileView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request):

        if not request.user.is_authenticated:
            return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        serializer = ProfileSerializer(request.user)
        return api_response(True, data=serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        if not request.user.is_authenticated:
            return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.update_password()
            login(request, user)
            return api_response(True, code=0)
        else:
            return api_response(False, code=403, message=get_error_message(serializer.errors), data=serializer.errors, status_code=status.HTTP_403_FORBIDDEN)
