from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.users.models import CustomUser
from apps.psychologists.models import ProfilePsychologist

from .models import Slot


def get_user_slot(user: CustomUser, pk: int) -> Slot:
    """Получение объекта Слот."""
    return get_object_or_404(Slot, psychologist__user=user, pk=pk)


def get_user_slots(user: CustomUser) -> QuerySet:
    psycho = get_object_or_404(ProfilePsychologist, user=user)
    return (psycho.slots.
            filter(datetime_from__gte=timezone.now()).
            select_related('session', 'session__client'))
