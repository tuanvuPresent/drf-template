from django.db.models import Q
from django_filters import NumberFilter, BaseInFilter, FilterSet
from django_filters.constants import EMPTY_VALUES


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class FilterSetMixin(object):

    @classmethod
    def get_filter_kwargs(cls, query_params):
        filter_kwargs = {}
        for name, field in cls.base_filters.items():
            value = query_params.get(name)
            if value not in EMPTY_VALUES and not field.exclude:
                lookup = f"{field.field_name}__{field.lookup_expr}"
                filter_kwargs[lookup] = value
        return Q(**filter_kwargs)


class BaseFilterSet(FilterSetMixin, FilterSet):
    pass
