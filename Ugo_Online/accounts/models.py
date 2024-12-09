from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('用户必须有一个邮箱地址')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser必须设置is_staff=True。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser必须设置is_superuser=True。')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('CUSTOMER', '买家'),
        ('SELLER', '卖家'),
    )
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=255, null=False)  # 用户名
    phone = models.CharField(unique=True, max_length=50, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')
    is_staff = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shops = models.ManyToManyField('shop.Shop', through='shop.SellerShop', related_name='sellers')

    objects = UserManager()

    USERNAME_FIELD = 'email'  # todo: 用用户名/手机号也可以登录，是否做？要保证用户名/手机号unique
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'[{self.email}] {self.name}'


class Address(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='addresses')
    recipient_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            # 将该用户的其他地址设为非默认
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.recipient_name} - {self.province}, {self.city}, {self.address}"

