from apps.core.filters import BaseFilterSet
from django_filters import CharFilter


class UserFilter(BaseFilterSet):
    username = CharFilter()
