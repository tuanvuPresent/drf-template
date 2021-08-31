from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.common.constant import ErrorCode
from apps.common.custom_exception_handler import CustomAPIException
from apps.user.models import User


class JWTLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=64, required=True, help_text='Leave empty if no change needed',
                                     style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError('password and username field required')

        user = authenticate(username=username, password=password)
        if not user:
            raise CustomAPIException(ErrorCode.LOGIN_FAIL)
        return user


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type']
