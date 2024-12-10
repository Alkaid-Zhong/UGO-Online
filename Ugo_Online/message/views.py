from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Ugo_Online.utils import api_response, list_response
from accounts.permissions import IsCustomer
from message.models import Message
from message.serializers import MessageSerializer


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_read']
    ordering_fields = ['created_time']
    ordering = ['-created_time']

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data).data
            return list_response(paginated_response, self.paginator, 'messages')
        else:
            serializer = self.get_serializer(queryset, many=True)
            return api_response(True, code=0, data={'messages': serializer.data})


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return api_response(success=True, data=MessageSerializer(message).data)


class ReadAllMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Message.objects.filter(user=request.user).update(is_read=True)
        return api_response(success=True, message='All messages have been read')


class HasUnreadMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        has_unread_message = Message.objects.filter(user=request.user, is_read=False).exists()
        unread_num = Message.objects.filter(user=request.user, is_read=False).count()
        return api_response(success=True, data={'has_unread_message': has_unread_message, 'unread_num': unread_num})
