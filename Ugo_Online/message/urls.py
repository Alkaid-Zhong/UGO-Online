from django.urls import path

from message.views import MessageListView, MessageView

urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:message_id>/', MessageView.as_view(), name='message_detail'),
]