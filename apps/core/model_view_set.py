from apps.authentication.jwt_authentication import JWTAuthentication
from apps.core.base_response import BaseResponse
from apps.core.serializer import NoneSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from apps.core.repository import RepositoryBase


class BaseGenericViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_action_classes = {}
    serializer_action_classes = {}
    serializer_class = NoneSerializer
    repository_class = RepositoryBase
    ordering_fields = None
    filterset_class = None
    filter_backends = [DjangoFilterBackend]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = None

    def get_permissions(self):
        try:
            permission_classes = self.permission_action_classes[self.action]
            return [permission() for permission in permission_classes]
        except (KeyError, AttributeError):
            return super().get_permissions()

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, args, kwargs)
        if isinstance(response, Response) and not response.exception:
            response.data = BaseResponse(data=response.data).data
        return response


    def get_queryset(self):
        self.queryset = self.repository_class.all()
        return self.queryset


    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = self.repository_class.get_object_or_404(queryset.model, filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class BaseCreateModelMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.repository_class.create(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)


class BaseRetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BaseUpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.repository_class.update(instance, serializer.validated_data)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(self.get_serializer(instance).data)


class BaseDestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.repository_class.delete(instance)
        return Response()


class FilterMixin:
    filterset_cleaned_data = {}

    def get_filter_kwargs(self):
        if not self.filterset_class:
            return Q()

        kwargs = DjangoFilterBackend().get_filterset_kwargs(self.request,
                                                            self.queryset,
                                                            self)
        filterset = self.filterset_class(**kwargs)
        if not filterset.is_valid():
            raise utils.translate_validation(filterset.errors)
        self.filterset_cleaned_data = filterset.form.cleaned_data
        return self.filterset_class.get_filter_kwargs(filterset.form.cleaned_data)


class BaseListModelMixin(FilterMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_kwargs = self.get_filter_kwargs()
        queryset = self.repository_class.filter_queryset(queryset, filter_kwargs=filter_kwargs)

        if self.ordering_fields:
            ordering = OrderingFilter().get_ordering(self.request, queryset, self)
            queryset = self.repository_class.ordering_queryset(queryset, ordering)
        if self.pagination_class is not None:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BaseModelViewSet(BaseCreateModelMixin,
                       BaseRetrieveModelMixin,
                       BaseUpdateModelMixin,
                       BaseDestroyModelMixin,
                       BaseListModelMixin,
                       BaseGenericViewSet):
    allow_action_name = ['create', 'list', 'retrieve', 'update', 'destroy', 'partial_update']

    def get_permissions(self):
        if self.action not in self.allow_action_name:
            raise MethodNotAllowed(self.action)
        return super().get_permissions()
