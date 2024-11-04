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
    phone = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')
    is_staff = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # todo: 用用户名/手机号也可以登录，是否做？要保证用户名/手机号unique
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

