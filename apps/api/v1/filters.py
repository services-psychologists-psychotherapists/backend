from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from apps.session.models import Slot


class TitleFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')


class InstituteFilter(TitleFilter):
    is_higher = filters.BooleanFilter()


class SlotFilter(filters.FilterSet):
    since = filters.DateFilter(method='filter_dates')
    
    class Meta:
        model = Slot
        fields = ('since',)

    def filter_dates(self, queryset, name, since):
        until = since + timedelta(days=14)
        return queryset.filter(datetime_from__gte=since, datetime_to__lte=until)
