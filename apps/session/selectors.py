from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.psychologists.models import ProfilePsychologist
from apps.users.models import CustomUser


def get_all_free_slots_by_user(user: CustomUser) -> QuerySet:
    """Возвращает все свободные слоты психолога."""
    psycho = get_object_or_404(ProfilePsychologist, user=user)
    return psycho.slots.filter(is_free=True).select_related(
        "session", "session__client"
    )


def get_all_slots_by_user(user: CustomUser) -> QuerySet:
    """Возвращает все слоты психолога."""
    psycho = get_object_or_404(ProfilePsychologist, user=user)
    return psycho.slots.select_related("session", "session__client")
