from django.shortcuts import get_object_or_404

from .models import Client


def get_client(user):
    return get_object_or_404(Client, user=user)
