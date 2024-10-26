from apps.authentication.serializer import JWTLoginSerializer, UserAccountSerializer, UserInfoSerializer
from apps.core.model_view_set import BaseGenericViewSet
from apps.authentication.signals import user_login, user_logout
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings


class JWTAuthAPIView(BaseGenericViewSet):
    serializer_action_classes = {
        'login': JWTLoginSerializer,
        'get_user_info': UserInfoSerializer,
    }

    @action(methods=['post'], detail=False)
    def logout(self, request):
        response = Response(data=None)
        response.delete_cookie(api_settings.JWT_AUTH_COOKIE)
        user_logout.send(sender=request.user.__class__, user=request.user)
        return response

    @action(methods=['post'], detail=False, authentication_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token = serializer.validated_data.get('token')

        data = {
            'token': token,
            'user': UserAccountSerializer(user).data
        }
        response = Response(data=data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)

        user_login.send(sender=request.user.__class__, user=user)
        return response

    @action(methods=['get'], detail=False, url_path='me')
    def get_user_info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
