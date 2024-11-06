from rest_framework import serializers
from .models import User

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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']

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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'role']
