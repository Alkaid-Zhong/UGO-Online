from django.shortcuts import render
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


def api_response(success, code=0, message='', data=None):
    return Response({
        'success': success,
        'code': code,
        'message': message,
        'data': data
    })


class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, message='注册成功')
        else:
            return api_response(False, code=1, message='注册失败', data=serializer.errors)


class SellerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MerchantRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, message='注册成功')
        else:
            return api_response(False, code=1, message='注册失败', data=serializer.errors)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return api_response(True, message='登录成功')
        else:
            return api_response(False, code=1, message='登录失败', data=serializer.errors)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return api_response(True, message='登出成功')


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return api_response(True, data=serializer.data)
