from django.db import models
from rest_framework.generics import get_object_or_404


class RepositoryBase(object):
    class Meta:
        model = models.Model

    @classmethod
    def all(cls):
        return cls.Meta.model.objects.all()

    @classmethod
    def count(cls, queryset):
        return queryset.count()

    @classmethod
    def get_object_or_404(cls, queryset, filter_kwargs):
        return get_object_or_404(queryset, **filter_kwargs)
    
    @classmethod
    def retrieve(cls, queryset, filter_kwargs):
        return get_object_or_404(queryset, **filter_kwargs)

    @classmethod
    def create(cls, data):
        return cls.Meta.model.objects.create(**data)

    @classmethod
    def update(cls, instance, data):
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()
        return instance

    @classmethod
    def filter_queryset(cls, queryset, filter_kwargs):
        return queryset.filter(filter_kwargs)

    @classmethod
    def paginate_queryset(cls, queryset, paginate):
        return list(queryset[paginate.offset:paginate.offset + paginate.limit])

    @classmethod
    def ordering_queryset(cls, queryset, ordering):
        return queryset.order_by(*ordering) if ordering else queryset

    @classmethod
    def save(cls, instance, update_fields=None):
        instance.save(update_fields=update_fields)
        return instance
