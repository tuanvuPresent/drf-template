from django_filters.rest_framework import DjangoFilterBackend
from apps.user.serializer import UserSerializer
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from apps.core.model_view_set import BaseModelViewSet
from apps.core.permission import IsAdminUser
from django.contrib.auth import get_user_model
from apps.user.filter import UserFilter
from apps.user.repository import UserRepository
User = get_user_model()


@method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class UserAPIView(BaseModelViewSet):
    serializer_action_classes = {
        'list': UserSerializer,
    }
    permission_action_classes = {
        'list': [IsAdminUser],
    }
    allow_action_name = ['list']
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    repository_class = UserRepository
