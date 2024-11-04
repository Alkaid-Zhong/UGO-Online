from rest_framework import serializers
from .models import User, MerchantProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MerchantRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    contact_info = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'name', 'contact_info', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        contact_info = validated_data.pop('contact_info', None)
        user = User(**validated_data)
        user.set_password(password)
        user.role = 'SELLER'
        user.save()
        if contact_info:
            MerchantProfile.objects.create(user=user, contact_info=contact_info)
        else:
            MerchantProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('用户不存在')
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户已被禁用')
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError('必须提供邮箱和密码')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'role']
