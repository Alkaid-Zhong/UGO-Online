from django.urls import path
from .views import (
    CustomerRegistrationView,
    SellerRegistrationView,
    LoginView,
    LogoutView,
    UserProfileView,
    ChangePasswordView
)

urlpatterns = [
    path('register/customer/', CustomerRegistrationView.as_view(), name='customer_register'),
    path('register/seller/', SellerRegistrationView.as_view(), name='seller_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name = 'change_password')
]
