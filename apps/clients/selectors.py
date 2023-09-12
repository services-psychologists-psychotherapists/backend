from django.shortcuts import get_object_or_404

from apps.users.models import CustomUser

from .models import Client


def get_client(user: CustomUser) -> Client:
    return get_object_or_404(Client, user=user)
