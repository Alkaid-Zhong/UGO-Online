from django.urls import path
from .views import ShopCreateView, ShopProfileView

urlpatterns = [
    path('create', ShopCreateView.as_view(), name='shop_create'),
    path('profile', ShopProfileView.as_view(), name='shop_profile'),
]