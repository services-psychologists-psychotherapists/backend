import threading

from django.http import HttpRequest
from rest_framework.exceptions import APIException

from apps.core.email import (
    ClientNewSessionEmail,
    ClientSessionCancellationEmail,
    PsychoNewSessionEmail,
    PsychoSessionCancellationEmail,
)
from apps.core.zoom import create_meeting

from .models import Slot


class SessionCancelEmailThread(threading.Thread):
    """Отправка писем об отмене сессии."""

    def __init__(self, request: HttpRequest, context: dict) -> None:
        self.request = request
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        ClientSessionCancellationEmail(
            request=self.request, context=self.context
        ).send(to=[self.context["client_email"]])

        PsychoSessionCancellationEmail(
            request=self.request, context=self.context
        ).send(to=[self.context["psychologist_email"]])


class ArrangeZoomSendEmailThread(threading.Thread):
    """Получение ссылок на встречи Zoom и информирование участников."""

    def __init__(
        self, slot: Slot, request: HttpRequest, context: dict
    ) -> None:
        self.slot = slot
        self.request = request
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        try:
            client_url, psycho_url = create_meeting(self.slot.datetime_from)
        except APIException:
            # продумать логику информирования администрации сайта
            # для подготовки ссылки вручную
            pass
        else:
            self.slot.session.client_link = client_url
            self.slot.session.psycho_link = psycho_url
            self.slot.session.save()
        finally:
            ClientNewSessionEmail(
                request=self.request, context=self.context
            ).send(to=[self.context["client_email"]])
            PsychoNewSessionEmail(
                request=self.request, context=self.context
            ).send(to=[self.context["psychologist_email"]])
