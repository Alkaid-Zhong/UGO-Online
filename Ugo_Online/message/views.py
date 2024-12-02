from django.shortcuts import render
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Ugo_Online.utils import api_response
from accounts.permissions import IsCustomer
from message.models import Message
from message.serializers import MessageSerializer


class MessageListView(ListView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return api_response(success=True, data=MessageSerializer(message).data)


