from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import GenericViewSet

from apps.authentication.custom_authentication import JWTAuthentication
from apps.common.custom_response import CustomResponse
from apps.common.serializer import NoneSerializer


class BaseGenericViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_action_classes = {}
    serializer_method_classes = None
    serializer_action_classes = None
    serializer_class = NoneSerializer

    filter_backends = [DjangoFilterBackend]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = None

    def get_permissions(self):
        try:
            permission_classes = self.permission_action_classes[self.action]
        except (KeyError, AttributeError):
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        try:
            if self.serializer_method_classes is not None:
                return self.serializer_method_classes[self.request.method]
            if self.serializer_action_classes is not None:
                return self.serializer_action_classes[self.action]

            return self.serializer_class
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def finalize_response(self, request, response, *args, **kwargs):
        if not response.exception:
            response.data = CustomResponse(data=response.data).data

        return super().finalize_response(request, response, args, kwargs)


class BaseModelViewSet(BaseGenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin):
    allow_action_name = ['create', 'list', 'retrieve', 'update', 'destroy', 'partial_update']

    def get_permissions(self):
        if self.action not in self.allow_action_name:
            raise MethodNotAllowed(self.action)
        try:
            permission_classes = self.permission_action_classes[self.action]
        except (KeyError, AttributeError):
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def destroy(self, request, *args, **kwargs):
        super(BaseModelViewSet, self).destroy(request, args, kwargs)
        return Response()
