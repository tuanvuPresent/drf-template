# Create your views here.
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from apps.authentication.serializer import JWTLoginSerializer, UserAccountSerializer
from apps.authentication.utils import jwt_payload_handler, jwt_encode_handler
from apps.common.custom_model_view_set import BaseGenericViewSet
from apps.user.models import Token


class JWTAuthAPIView(BaseGenericViewSet):
    serializer_action_classes = {
        'login': JWTLoginSerializer,
    }

    @action(methods=['get'], detail=False)
    def logout(self, request):
        Token.objects.filter(user=request.user, token=request.auth.token).delete()
        response = Response(data=None)
        response.delete_cookie(api_settings.JWT_AUTH_COOKIE)
        return response

    @swagger_auto_schema(request_body=JWTLoginSerializer)
    @action(methods=['post'], detail=False, authentication_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        time_token = datetime.utcnow().timestamp()
        Token.objects.create(user=user, token=time_token)
        payload = jwt_payload_handler(user, time_token)
        token = jwt_encode_handler(payload)
        data = {
            'token': token,
            'user': UserAccountSerializer(user).data
        }
        response = Response(data=data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response
