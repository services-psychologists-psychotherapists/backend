from dateutil.relativedelta import relativedelta

from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.core.constants import LOADED_DAYS_FOR_SLOTS
from apps.psychologists.models import (
    ProfilePsychologist,
    PsychoEducation,
    Service,
)
from apps.users.models import CustomUser
from apps.session.models import Slot


def get_psychologist(user: CustomUser) -> ProfilePsychologist:
    queryset = (
        ProfilePsychologist.objects.all()
        .select_related("user")
        .prefetch_related(
            Prefetch("themes"),
            Prefetch("approaches"),
            Prefetch("education"),
        )
    )
    return get_object_or_404(queryset, user=user)


def get_all_verified_psychologists() -> list[ProfilePsychologist]:
    return (
        ProfilePsychologist.objects.filter(is_verified=True)
        .prefetch_related(
            Prefetch("slots"),
            Prefetch("services"),
        )
        .order_by("id")
    )


def get_psychologist_for_card(id) -> ProfilePsychologist:
    queryset = (
        ProfilePsychologist.objects.all()
        .select_related("user")
        .prefetch_related(
            Prefetch("themes"),
            Prefetch("approaches"),
            Prefetch("education"),
            Prefetch("slots"),
            Prefetch("services"),
        )
    )
    return get_object_or_404(queryset, id=id)


def get_psychologist_with_services(id: int) -> ProfilePsychologist:
    """Выдача психолога с присоединенной таблицей сервисов."""
    queryset = ProfilePsychologist.objects.all().prefetch_related(
        Prefetch("services"),
    )
    return get_object_or_404(queryset, id=id)


def get_education(
    user: ProfilePsychologist, flag: bool
) -> list[PsychoEducation]:
    return PsychoEducation.objects.filter(
        psychologist=user, institute__is_higher=flag
    ).select_related("document")


def get_price(psychologist: ProfilePsychologist) -> Service:
    prices = Service.objects.filter(psychologist=psychologist).values_list(
        "price", flat=True)
    if prices:
        return min(prices)
    return 1


def get_free_slots(psychologist: ProfilePsychologist) -> Slot:
    now = timezone.now()
    finish = now + relativedelta(days=+LOADED_DAYS_FOR_SLOTS)
    slots = Slot.objects.filter(
        psychologist=psychologist,
        is_free=True,
        datetime_from__gt=now,
        datetime_to__lte=finish,
    )
    return slots


def get_all_free_slots(psychologist_id: int) -> QuerySet:
    """Возвращает все свободные слоты психолога с текущего момента."""
    psycho = get_object_or_404(ProfilePsychologist, pk=psychologist_id)
    now = timezone.now()
    return psycho.slots.filter(datetime_from__gte=now, is_free=True)
