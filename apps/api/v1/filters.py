from datetime import timedelta

from django_filters import rest_framework as filters

from apps.core.constants import LOADED_DAYS_IN_CALENDAR
from apps.core.models import Gender
from apps.psychologists.models import ProfilePsychologist, Theme
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


class NumberRangeFilter(filters.BaseRangeFilter, filters.NumberFilter):
    def get_filter_predicate(self, v):
        a = 1
        return {'age': v.age,
                'experience': v.experience,
                }

    def filter(self, qs, value):
        if value:
            qs = qs.annotate_property_field()
            qs = super().filter(qs, value)
        return qs


class PsychoFilter(filters.FilterSet):
    gender = filters.ChoiceFilter(choices=Gender.choices)
    themes = filters.ModelMultipleChoiceFilter(
        field_name='themes__title',
        to_field_name='title',
        queryset=Theme.objects.all(),
    )
    age = NumberRangeFilter(field_name='age', lookup_expr='range')
    # age = filters.RangeFilter(field_name='age')

    class Meta:
        model = ProfilePsychologist
        fields = ('gender', 'themes', 'approaches', 'age')
