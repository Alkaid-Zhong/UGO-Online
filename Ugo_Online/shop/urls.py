from django.urls import path
from .views import (ShopCreateView, ShopInfoView,
                    ShopListView, CreateInvitationCodeView,
                    JoinShopByCodeView, AddProductView,
                    ProductListView, CategoryListView)

urlpatterns = [
    path('', ShopListView.as_view(), name='get_all_shop'),
    path('create', ShopCreateView.as_view(), name='shop_create'),
    path('<int:id>/info', ShopInfoView.as_view(), name='shop_info'),
    path('<int:id>/create_invitation_code', CreateInvitationCodeView.as_view(), name='create_invitation_code'),
    path('join_by_code', JoinShopByCodeView.as_view(), name='join_by_code'),
    path('<int:id>/product/add', AddProductView.as_view(), name='add_product'),
    path('<int:shop_id>/products', ProductListView.as_view(), name='get_shop_products'),
    path('products', ProductListView.as_view(), name='get_products'),
    path('category_list', CategoryListView.as_view(), name='category_list'),
    path('<int:shop_id>/category_list', CategoryListView.as_view(), name='shop_category_list'),
]