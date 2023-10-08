import threading

from apps.core.email import PsychologistActivationEmail


class PsychoActivationEmailThread(threading.Thread):
    """Отправка письма клиенту для подтверждения электронной почты."""

    def __init__(self, request, psychologist):
        self.request = request
        self.psychologist = psychologist
        threading.Thread.__init__(self)

    def run(self):
        PsychologistActivationEmail(
            request=self.request,
            context={"user": self.psychologist.user},
        ).send(to=[self.psychologist.user.email])
