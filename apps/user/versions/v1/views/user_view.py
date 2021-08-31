# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsAdminUser
from apps.user.models import User
from apps.user.serializer import UserSerializer


@method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class UserAPIView(BaseModelViewSet):
    serializer_action_classes = {
        'list': UserSerializer,
    }

    permission_action_classes = {
        'list': [IsAdminUser],
    }
    allow_action_name = ['list']

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        return queryset
