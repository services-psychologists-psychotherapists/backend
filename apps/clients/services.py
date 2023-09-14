from typing import OrderedDict

from django.db.transaction import atomic
from django.http import HttpRequest

from apps.users.models import CustomUser

from .models import Client
from .threads import ClientActivationEmailThread


@atomic
def create_client(
    user_data: OrderedDict, client_data: OrderedDict, request: HttpRequest
) -> tuple[CustomUser, Client]:
    """
    Создание пользователя, создание клиента, отправка письма клиенту со ссылкой
    для подтверждения почты и активации аккаунта.
    """
    user = CustomUser.objects.create_user(**user_data)
    client = Client.objects.create(user=user, **client_data)

    ClientActivationEmailThread(request, user).start()

    return user, client


def update_client(client: Client, data: OrderedDict) -> Client:
    """Обновление профиля клиента."""
    for key, value in data.items():
        setattr(client, key, value)
    client.save()
    return client
