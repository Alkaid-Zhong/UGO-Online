from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from .serializers import (
    UserRegistrationSerializer,
    MerchantRegistrationSerializer,
    LoginSerializer,
    UserProfileSerializer
)
from .models import User


def get_error_message(errors):
    """
    从 serializer.errors 中提取错误信息，返回一个中文字符串
    """
    messages = []
    for field, error_list in errors.items():
        for error in error_list:
            return str(error)
            # messages.append(str(error))
    return "，".join(messages)


def api_response(success, code=0, message='', data=None, status_code=status.HTTP_200_OK):
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

    @csrf_exempt
    def get(self, request):

        if not request.user.is_authenticated:
            return api_response(False, code=401, message='用户未登录', status_code=status.HTTP_401_UNAUTHORIZED)

        serializer = UserProfileSerializer(request.user)
        return api_response(True, data=serializer.data)
