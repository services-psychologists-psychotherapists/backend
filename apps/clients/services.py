from django.db.transaction import atomic

from apps.users.models import CustomUser

from .models import Client


@atomic
def create_client(user_data, client_data):
    user = CustomUser.objects.create_user(**user_data)
    return Client.objects.create(user=user, **client_data)


def update_client(client, data):
    for key, value in data.items():
        setattr(client, key, value)
    client.save()
    return client
