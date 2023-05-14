from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'gender', 'user_type')
