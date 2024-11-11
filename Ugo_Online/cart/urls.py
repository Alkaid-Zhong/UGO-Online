from django.urls import path
from .views import (
    CartItemView,
    CartDetailView
)

urlpatterns = [
    path('add', CartItemView.as_view(), name='add_product2cart'),
    path('update', CartItemView.as_view(), name='item_update'),
    path('delete', CartItemView.as_view(), name='item_delete'),
    path('', CartDetailView.as_view(), name='cart_detail')
]
