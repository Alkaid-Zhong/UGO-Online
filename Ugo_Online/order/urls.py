from django.urls import path
from .views import CreateOrderView, UserOrderListView, SellerOrderListView, OrderDetailView, OrderPaymentView, \
    CancelOrderView, UpdateOrderStatus2ShippedView, RefundOrderItemsView, UpdateOrderStatus2CompletedView, \
    UpdateOrderAddressView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='order_create'),
    path('user_orders/', UserOrderListView.as_view(), name='user_orders'),
    path('seller_orders/<int:shop_id>/', SellerOrderListView.as_view(), name='seller_orders'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('pay/', OrderPaymentView.as_view(), name='order-payment'),
    path('<int:order_id>/cancel/', CancelOrderView.as_view(), name='order-cancel'),
    path('<int:order_id>/refund/', RefundOrderItemsView.as_view(), name='order-refund'),
    path('<int:order_id>/ship/', UpdateOrderStatus2ShippedView.as_view(), name='order-ship'),
    path('<int:order_id>/complete/', UpdateOrderStatus2CompletedView.as_view(), name='order-complete'),
    path('<int:order_id>/update_address/', UpdateOrderAddressView.as_view(), name='order-update-address'),
]
