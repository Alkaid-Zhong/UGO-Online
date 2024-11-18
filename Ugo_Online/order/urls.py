from django.urls import path
from .views import CreateOrderView, UserOrderListView, SellerOrderListView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='order_create'),
    path('user_orders/', UserOrderListView.as_view(), name='user_orders'),
    path('seller_orders/<int:shop_id>/', SellerOrderListView.as_view(), name='seller_orders'),
]
