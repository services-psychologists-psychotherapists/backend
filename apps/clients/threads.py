import threading

from django.http import HttpRequest

from apps.core.email import ClientActivationEmail
from apps.users.models import CustomUser


class ClientActivationEmailThread(threading.Thread):
    """Отправка письма клиенту для подтверждения электронной почты."""

    def __init__(self, request: HttpRequest, user: CustomUser):
        self.request = request
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        ClientActivationEmail(
            request=self.request,
            context={"user": self.user},
        ).send(to=[self.user.email])
