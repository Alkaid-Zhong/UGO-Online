from django.urls import path
from .views import ShopCreateView

urlpatterns = [
    path('create', ShopCreateView.as_view(), name='shop_create'),
]