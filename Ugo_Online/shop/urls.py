from django.urls import path
from .views import ShopCreateView, ShopInfoView, AllShopView

urlpatterns = [
    path('', AllShopView.as_view(), name='get_all_shop'),
    path('create', ShopCreateView.as_view(), name='shop_create'),
    path('<int:id>/info', ShopInfoView.as_view(), name='shop_info'),
]