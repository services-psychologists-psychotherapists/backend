import threading

from apps.core.email import (
    PsychoActivationEmail,
    PsychoConfirmationFormEmail,
)


class PsychoActivationEmailThread(threading.Thread):
    """Отправка письма психологу для активации аккаунта"""

    def __init__(self, psychologist):
        self.psychologist = psychologist
        threading.Thread.__init__(self)

    def run(self):
        PsychoActivationEmail(
            context={"user": self.psychologist.user},
        ).send(to=[self.psychologist.user.email])


class PsychoConfirmationFormEmailThread(threading.Thread):
    """Отправка письма психологу, что анкета получена"""

    def __init__(self, request, user):
        self.request = request
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        PsychoConfirmationFormEmail(
            request=self.request,
            context={"user": self.user},
        ).send(to=[self.user.email])
        print("email to confirm form send")
