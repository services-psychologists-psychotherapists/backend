import threading

from apps.core.email import (ClientSessionCancellationEmail,
                             PsychoSessionCancellationEmail)

from .models import Session


class SessionCancelEmailThread(threading.Thread):
    """Отправка писем об отмене сессии."""
    def __init__(self, session: Session, initiator: str,
                 late_cancel: bool) -> None:
        self.session = session
        self.initiator = initiator
        self.late_cancel = late_cancel
        threading.Thread.__init__(self)

    def run(self):
        context = {
            'session': self.session,
            'initiator': self.initiator,
            'late_cancel': self.late_cancel,
        }

        ClientSessionCancellationEmail(
            context=context
        ).send(to=[self.session.client.user.email])

        PsychoSessionCancellationEmail(
            context=context
        ).send(to=[self.session.slot.psychologist.user.email])
