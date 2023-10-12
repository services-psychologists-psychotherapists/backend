from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django_filters import rest_framework as filters

from apps.core.constants import LOADED_DAYS_IN_CALENDAR
from apps.core.models import Gender
from apps.psychologists.models import ProfilePsychologist, Theme, Approach
from apps.session.models import Slot


class TitleFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")


class InstituteFilter(TitleFilter):
    is_higher = filters.BooleanFilter()


class SlotFilter(filters.FilterSet):
    """Фильтрация слотов по их дате."""

    since = filters.DateFilter(method="filter_dates", required=True)

    class Meta:
        model = Slot
        fields = ("since",)

    def filter_dates(self, queryset, name, since):
        until = since + timedelta(days=LOADED_DAYS_IN_CALENDAR)
        return queryset.filter(
            datetime_from__gte=since, datetime_from__lte=until
        )


def filter_property(queryset, value, field):
    today = date.today()
    if value.start is not None and value.stop is not None:
        value = (value.start, value.stop)
        start = today - relativedelta(years=+value[1])
        finish = today - relativedelta(years=+value[0])
        lookup = "__".join([field, "range"])
        qs = queryset.filter(**{lookup: [start, finish]})
    elif value.start is not None:
        value = value.start
        finish = today - relativedelta(years=+value)
        lookup = "__".join([field, "lte"])
        qs = queryset.filter(**{lookup: finish})
    elif value.stop is not None:
        value = value.stop
        start = today - relativedelta(years=+value)
        lookup = "__".join([field, "gte"])
        qs = queryset.filter(**{lookup: start})
    return qs


class PsychoFilter(filters.FilterSet):
    gender = filters.ChoiceFilter(choices=Gender.choices)
    themes = filters.ModelMultipleChoiceFilter(
        field_name="themes__title",
        to_field_name="title",
        queryset=Theme.objects.all(),
    )
    approaches = filters.ModelMultipleChoiceFilter(
        field_name="approaches__title",
        to_field_name="title",
        queryset=Approach.objects.all(),
    )
    age = filters.RangeFilter(method="filter_age")
    experience = filters.RangeFilter(method="filter_experience")

    class Meta:
        model = ProfilePsychologist
        fields = ("gender", "themes", "approaches", "age", "experience")

    def filter_age(self, queryset, name, value):
        if value:
            queryset = filter_property(queryset, value, "birthday")
        return queryset

    def filter_experience(self, queryset, name, value):
        if value:
            queryset = filter_property(queryset, value, "started_working")
        return queryset
