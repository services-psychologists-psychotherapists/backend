from django.db.models import Min, Value
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.core.constants import SESSION_DURATION
from apps.users.models import CustomUser

from .models import Client
from apps.psychologists.models import ProfilePsychologist
from apps.session.models import Session


def get_client(user: CustomUser) -> Client:
    return get_object_or_404(Client, user=user)


def get_next_session(client: Client) -> Session:
    """Возвращает ближайшую сессию клиента с допуском в 30 минут."""
    now = timezone.now()
    # включение уже начавшейся сессии на случай опоздания в пределах 30 минут
    if now.minute <= 30:
        now = now.replace(minute=0, second=0, microsecond=0)
    return (
        Session.objects.
        filter(
            slot__datetime_from__gte=now,
            status=Session.StatusChoice.PAID,
            client=client,
        ).
        order_by('slot__datetime_from').
        select_related('slot', 'service', 'slot__psychologist').
        first()
    )


def get_my_psychologist(client: Client) -> ProfilePsychologist:
    """Возвращает психолога из последней прошедшей сессии."""
    now = timezone.now()
    return (
        ProfilePsychologist.objects.
        filter(slots__session__client=client, slots__datetime_from__lt=now).
        order_by('slots__datetime_from').
        annotate(
            price=Min('services__price'),
            duration=Value(SESSION_DURATION),
        ).
        last()
    )
