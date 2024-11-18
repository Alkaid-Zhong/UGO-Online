from django.urls import path
from .views import CreateOrderView, UserOrderListView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='order_create'),
    path('user_orders/', UserOrderListView.as_view(), name='user_orders'),
]
