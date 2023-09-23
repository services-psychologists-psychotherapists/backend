from datetime import timedelta

from django_filters import rest_framework as filters

from apps.core.constants import LOADED_DAYS_IN_CALENDAR
from apps.session.models import Slot


class TitleFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')


class InstituteFilter(TitleFilter):
    is_higher = filters.BooleanFilter()


class SlotFilter(filters.FilterSet):
    """Фильтрация слотов по их дате."""
    since = filters.DateFilter(method='filter_dates')

    class Meta:
        model = Slot
        fields = ('since',)

    def filter_dates(self, queryset, name, since):
        until = since + timedelta(days=LOADED_DAYS_IN_CALENDAR)
        return queryset.filter(
            datetime_from__gte=since,
            datetime_to__lte=until
        )
