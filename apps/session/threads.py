import threading

from rest_framework.exceptions import APIException

from apps.core.email import (ClientSessionCancellationEmail,
                             NewSessionEmail,
                             PsychoSessionCancellationEmail)
from apps.core.zoom import create_meeting

from .models import Session, Slot


class SessionCancelEmailThread(threading.Thread):
    """Отправка писем об отмене сессии."""
    def __init__(self, context: dict) -> None:
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        ClientSessionCancellationEmail(
            context=self.context
        ).send(to=[self.context['client_email']])

        PsychoSessionCancellationEmail(
            context=self.context
        ).send(to=[self.context['psychologist_email']])


class ArrangeZoomSendEmailThread(threading.Thread):
    """Получение ссылок на встречи Zoom и информирование участников."""
    def __init__(self, session: Session, slot: Slot) -> None:
        self.session = session
        self.slot = slot
        threading.Thread.__init__(self)

    def run(self):
        try:
            client_url, psycho_url = create_meeting(self.slot.datetime_from)
        except APIException:
            # продумать логику информирования администрации сайта
            # для подготовки ссылки вручную
            pass
        else:
            self.session.client_link = client_url
            self.session.psycho_link = psycho_url
            self.session.save()
        finally:
            NewSessionEmail().send([self.session.client.user.email])
            NewSessionEmail().send([self.session.slot.psychologist.user.email])
