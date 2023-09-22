from django.db.models import F
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone

from apps.psychologists.models import ProfilePsychologist

from .models import Slot


def get_user_slot(user, pk):
    return get_object_or_404(Slot, user=user, pk=pk)


def get_user_slots(user):
    psycho = get_object_or_404(ProfilePsychologist, user=user)
    return psycho.slots.filter(datetime_from__gte=timezone.now()).select_related('session', 'session__client')


def get_free_slots(psychologist):
    now = timezone.now()
    return psychologist.slots.filter(datetime_from__gt=now, is_free=True)
