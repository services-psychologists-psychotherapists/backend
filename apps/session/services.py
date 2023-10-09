from datetime import datetime

from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.core.constants import NON_PENALTY_PERIOD
from apps.users.models import CustomUser

from .models import Session, Slot
from .threads import ArrangeZoomSendEmailThread, SessionCancelEmailThread


def create_session(user: CustomUser, slot: Slot) -> Session:
    """
    Создание сессии;
    В отдельном потоке: получение ссылок и рассылка эл.писем участникам.
    """
    with atomic():
        # пока используется только один сервис; впоследствии изменим логику
        price = slot.psychologist.services.first().price
        slot.is_free = False
        slot.save()
        session = Session.objects.create(
            client=user.client,
            slot=slot,
            price=price,
        )

    ArrangeZoomSendEmailThread(session=session, slot=slot).run()
    return session


def _form_context(session: Session, initiator: str, late_cancel: bool) -> dict:
    """Формирование контекста для отправки писем об отмене сессии."""
    return {
        'initiator': initiator,
        'late_cancel': late_cancel,
        'client_email': session.client.user.email,
        'psychologist_email': session.slot.psychologist.user.email,
    }


def _check_if_late(start: datetime) -> bool:
    """Проверка поздней отмены сессии клиентом."""
    now = timezone.now()
    diff = start - now
    return diff.total_seconds() / 3600 < NON_PENALTY_PERIOD


def _get_response_details(user: CustomUser, late_cancel: bool) -> dict:
    """Текст ответа в API при отмене сессии - возврат ден.средств."""
    refund = ''
    if user.is_client:
        if late_cancel:
            refund = ('Вы отменили позднее чем за 12 часов до начала, '
                      'поэтому оплата не возвращается.')
        else:
            refund = 'Оплата вернется в течение 7 дней.'
    return {'details': refund}


def cancel_session(user: CustomUser, session_id: int) -> dict:
    """Отмена сессии и рассылка эл.писем участникам."""
    queryset = Session.objects.select_related(
        'client',
        'client__user',
        'slot',
        'slot__psychologist',
        'slot__psychologist__user',
    )

    with atomic():
        session = get_object_or_404(queryset, id=session_id)
        slot = session.slot
        slot.is_free = True
        slot.save()

        start = slot.datetime_from
        late_cancel = False if user.is_psychologists else _check_if_late(start)
        initiator = 'psychologist' if user.is_psychologists else 'client'
        context = _form_context(session, initiator, late_cancel)

        session.delete()

    SessionCancelEmailThread(context).run()
    return _get_response_details(user, late_cancel)


def delete_user_slot(user: CustomUser, pk: int) -> None:
    """
    Удаление психологом слота из расписания.
    Если слот занят сессией, участники получают уведомление по почте.
    """
    slot = get_object_or_404(Slot, psychologist__user=user, pk=pk)

    if not slot.is_free:
        context = _form_context(slot.session, 'psychologist', False)
        SessionCancelEmailThread(context).run()

    slot.delete()
    return None
