from datetime import datetime, timedelta

from django.db.transaction import atomic
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.core.constants import NON_PENALTY_PERIOD
from apps.users.models import CustomUser

from .models import Session, Slot
from .threads import ArrangeZoomSendEmailThread, SessionCancelEmailThread


def get_session_context(session: Session) -> dict:
    """Формирование контекста для отправки писем о новой сессии."""
    moscow_datetime = session.slot.datetime_from + timedelta(hours=3)
    return {
        "client_name": session.client.get_full_name(),
        "psycho_name": session.slot.psychologist.get_full_name(),
        "date": moscow_datetime.date(),
        "time": moscow_datetime.time(),
        "client_email": session.client.user.email,
        "psychologist_email": session.slot.psychologist.user.email,
    }


def get_cancel_session_context(session: Session, refund: str) -> dict:
    """Формирование контекста для отправки писем об отмене сессии."""
    context = get_session_context(session=session)
    context["refund"] = refund
    return context


def check_if_late(start: datetime) -> bool:
    """Проверка поздней отмены сессии клиентом."""
    now = timezone.now()
    diff = start - now
    return diff.total_seconds() / 3600 < NON_PENALTY_PERIOD


def get_refund_text(user: CustomUser, late_cancel: bool = False) -> str:
    """Текст ответа в API при отмене сессии - возврат ден.средств."""
    refund = ""
    if user.is_client:
        if late_cancel:
            refund = (
                "Вы отменили позднее чем за 12 часов до начала, "
                "поэтому оплата не возвращается."
            )
        else:
            refund = "Оплата вернется в течение 7 дней."
    return refund


def create_session(request: HttpRequest, slot: Slot) -> Session:
    """
    Создание сессии;
    В отдельном потоке: получение ссылок и рассылка эл.писем участникам.
    """
    user = request.user
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

    context = get_session_context(session=session)
    ArrangeZoomSendEmailThread(
        slot=slot, context=context, request=request
    ).start()
    return session


def cancel_session(request: HttpRequest, session_id: int) -> dict:
    """Отмена сессии и рассылка эл.писем участникам."""
    user = request.user
    queryset = Session.objects.select_related(
        "client",
        "client__user",
        "slot",
        "slot__psychologist",
        "slot__psychologist__user",
    )

    with atomic():
        session = get_object_or_404(queryset, id=session_id)
        slot = session.slot
        slot.is_free = True
        slot.save()

        start = slot.datetime_from
        late_cancel = False if user.is_psychologists else check_if_late(start)
        refund = get_refund_text(user, late_cancel)
        context = get_cancel_session_context(session, refund)

        session.delete()

    SessionCancelEmailThread(request=request, context=context).start()
    return {"details": refund}


def delete_user_slot(request: HttpRequest, pk: int) -> None:
    """
    Удаление психологом слота из расписания.
    Если слот занят сессией, участники получают уведомление по почте.
    """
    user = request.user
    slot = get_object_or_404(Slot, psychologist__user=user, pk=pk)

    if not slot.is_free:
        refund = get_refund_text(user=user)
        context = get_cancel_session_context(
            session=slot.session, refund=refund
        )
        SessionCancelEmailThread(request=request, context=context).start()

    slot.delete()
    return None
