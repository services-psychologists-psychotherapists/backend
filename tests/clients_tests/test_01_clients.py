from http import HTTPStatus

import pytest
from rest_framework.reverse import reverse

from . import utils


@pytest.mark.django_db()
class Test01Client:
    @pytest.mark.parametrize("data,messege", utils.CLIENT_CREATE_VALID_DATA)
    def test_01_create_client_success(self, guest_client, data, messege):
        """Создание пользователя с валидными данными."""
        url = reverse("create_client")
        response = guest_client.post(url, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            f"POST-Запрос на создание клиента с валидными данными {messege}"
            f"возвращает статус {response.status_code}."
        )

    @pytest.mark.parametrize("data,messege", utils.CLIENT_CREATE_INVALID_DATA)
    def test_02_create_client_fail(self, guest_client, data, messege):
        """Создание пользователя с невалидными данными."""
        url = reverse("create_client")
        response = guest_client.post(url, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-Запрос на создание клиента с невалидными данными ({messege})"
            f"возвращает статус {response.status_code}."
        )
