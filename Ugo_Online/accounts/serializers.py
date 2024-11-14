from rest_framework import serializers
from .models import User
from shop.models import SellerShop



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, error_messages={
        'required': '密码不能为空',
        'blank': '密码不能为空',
    })
    email = serializers.EmailField(error_messages={
        'required': '邮箱不能为空',
        'blank': '邮箱不能为空',
        'invalid': '请输入有效的邮箱地址',
    })
    name = serializers.CharField(error_messages={
        'required': '用户名不能为空',
        'blank': '用户名不能为空',
    })

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class MerchantRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, error_messages={
        'required': '密码不能为空',
        'blank': '密码不能为空',
    })
    email = serializers.EmailField(error_messages={
        'required': '邮箱不能为空',
        'blank': '邮箱不能为空',
        'invalid': '请输入有效的邮箱地址',
    })
    name = serializers.CharField(error_messages={
        'required': '用户名不能为空',
        'blank': '用户名不能为空',
    })

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.role = 'SELLER'
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            'required': '邮箱不能为空',
            'blank': '邮箱不能为空',
            'invalid': '请输入有效的邮箱地址',
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '密码不能为空',
            'blank': '密码不能为空',
        }
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({'error': '用户不存在'})
            if not user.check_password(password):
                raise serializers.ValidationError({'error': '密码错误'})
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError({'error': '必须提供邮箱和密码'})


class ProfileSerializer(serializers.ModelSerializer):
    shop = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'shop']

    def get_shop(self, obj):
        try:
            seller_shop = SellerShop.objects.get(seller=obj)
            return seller_shop.shop.id  # 返回商店的 ID
        except SellerShop.DoesNotExist:
            return None



class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '密码不能为空',
            'blank': '密码不能为空',
        }
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': '密码不能为空',
            'blank': '密码不能为空',
        }
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password_confirm']

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'error': '旧密码不正确'})
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'error': '两次输入的密码不一致'})
        return data

    def update_password(self):
        user = self.context['request'].user
        new_password = self.validated_data['password']

        user.set_password(new_password)
        user.save()
        return user

