from typing import OrderedDict

from django.db.transaction import atomic

from apps.users.models import CustomUser

from .models import Client


@atomic
def create_client(
    user_data: OrderedDict, client_data: OrderedDict
) -> tuple[CustomUser, Client]:
    user = CustomUser.objects.create_user(**user_data)
    client = Client.objects.create(user=user, **client_data)
    return user, client


def update_client(client: Client, data: OrderedDict) -> Client:
    for key, value in data.items():
        setattr(client, key, value)
    client.save()
    return client
