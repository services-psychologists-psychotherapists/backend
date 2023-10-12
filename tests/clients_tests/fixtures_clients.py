import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.clients.models import Client


@pytest.fixture
def client_user(django_user_model):
    return django_user_model.objects.create_user(
        email="client_user@unexistingmail.ru",
        password="zz11xx22cc33",
        is_active=True,
    )


@pytest.fixture
def client_profile(client_user):
    return Client.objects.create(
        user=client_user,
        first_name="Макс",
        birthday="01.01.1980",
    )


@pytest.fixture
def client_token(client_user):
    token = AccessToken.for_user(client_user)
    return {"access": str(token)}


@pytest.fixture
def client_client(client_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'JWT {client_token["access"]}')
    return client
