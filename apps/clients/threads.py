import threading

from apps.core.email import ClientActivationEmail


class ClientActivationEmailThread(threading.Thread):
    """Отправка письма клиенту для подтверждения электронной почты."""
    def __init__(self, request, user):
        self.request = request
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        ClientActivationEmail(
            request=self.request,
            context={'user': self.user},
        ).send(to=[self.user.email])
