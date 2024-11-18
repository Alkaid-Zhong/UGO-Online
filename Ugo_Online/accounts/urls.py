from django.urls import path
from .views import (
    CustomerRegistrationView, SellerRegistrationView,
    LoginView, LogoutView,
    UserProfileView, ChangePasswordView,
    AddressCreateView, AddressListView,
    DefaultAddressView, AddressDeleteView,
    AddressDetailView, AddressUpdateView, AddMoneyView
)

urlpatterns = [
    path('register/customer/', CustomerRegistrationView.as_view(), name='customer_register'),
    path('register/seller/', SellerRegistrationView.as_view(), name='seller_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('address/create/', AddressCreateView.as_view(), name='address_create'),
    path('address/list/', AddressListView.as_view(), name='address_list'),
    path('address/default/', DefaultAddressView.as_view(), name='default_address'),
    path('address/<int:address_id>/delete/', AddressDeleteView.as_view(), name='address_delete'),
    path('address/<int:address_id>/', AddressDetailView.as_view(), name='address_detail'),
    path('address/<int:address_id>/update/', AddressUpdateView.as_view(), name='address_update'),
    path('add-money/', AddMoneyView.as_view(), name='add_money'),
]
