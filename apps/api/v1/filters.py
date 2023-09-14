from django_filters import rest_framework as filters


class TitleFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')


class InstituteFilter(TitleFilter):
    is_higher = filters.BooleanFilter()
