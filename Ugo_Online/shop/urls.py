from django.urls import path
from .views import (ShopCreateView, ShopInfoView,
                    ShopListView, CreateInvitationCodeView,
                    JoinShopByCodeView, AddProductView,
                    ProductListView, CategoryListView,
                    ShopTransactionListView, ReviewCreateView,
                    ReviewReplyView, ProductDetailView,
                    ProductReviewListView, OrderItemReviewView,
                    ShopOwnersView, ShopCommissionView)

urlpatterns = [
    path('', ShopListView.as_view(), name='get_all_shop'),
    path('create/', ShopCreateView.as_view(), name='shop_create'),
    path('<int:id>/info/', ShopInfoView.as_view(), name='shop_info'),
    path('<int:id>/create_invitation_code/', CreateInvitationCodeView.as_view(), name='create_invitation_code'),
    path('join_by_code/', JoinShopByCodeView.as_view(), name='join_by_code'),
    path('<int:id>/product/add/', AddProductView.as_view(), name='add_product'),
    path('<int:id>/product/update/', AddProductView.as_view(), name='update_product'),
    path('<int:id>/product/delete/', AddProductView.as_view(), name='delete_product'),
    path('<int:shop_id>/products/', ProductListView.as_view(), name='get_shop_products'),
    path('products/', ProductListView.as_view(), name='get_products'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('<int:shop_id>/category_list/', CategoryListView.as_view(), name='shop_category_list'),
    path('<int:shop_id>/transactions/', ShopTransactionListView.as_view(), name='shop_transactions'),
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
    path('review/<int:review_id>/reply/', ReviewReplyView.as_view(), name='reply_review'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/reviews/', ProductReviewListView.as_view(), name='product_reviews'),
    path('order_item/<int:order_item_id>/review/', OrderItemReviewView.as_view(), name='order_item_review'),
    path('<int:shop_id>/owners/', ShopOwnersView.as_view(), name='shop_owners'),
    path('<int:shop_id>/split/', ShopCommissionView.as_view(), name='shop_split')
]
