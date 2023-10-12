from http import HTTPStatus

import pytest
from rest_framework.reverse import reverse

from . import utils


@pytest.mark.django_db()
class Test01Client:
    profile_url = reverse("client_profile")
    create_url = reverse("create_client")

    @pytest.mark.parametrize("data,messege", utils.CLIENT_CREATE_VALID_DATA)
    def test_01_create_client_success(self, guest_client, data, messege):
        """Создание пользователя с валидными данными."""
        response = guest_client.post(self.create_url, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            f"POST-Запрос на создание клиента с валидными данными {messege}"
            f"возвращает статус {response.status_code}."
        )

    @pytest.mark.parametrize("data,messege", utils.CLIENT_CREATE_INVALID_DATA)
    def test_02_create_client_fail(self, guest_client, data, messege):
        """Создание пользователя с невалидными данными."""
        response = guest_client.post(self.create_url, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"POST-Запрос на создание клиента с невалидными данными ({messege})"
            f"возвращает статус {response.status_code}."
        )

    @pytest.mark.parametrize("data,messege", utils.CLIENT_UPDATE_VALID_DATA)
    def test_03_update_client_success(self, client_client, data, messege):
        """Изменение профиля клиента с валидными данными."""
        response = client_client.put(self.profile_url, data=data)
        assert response.status_code == HTTPStatus.OK, (
            f"POST-Запрос на изменение профиля клиента с валидными данными {messege}"
            f"возвращает статус {response.status_code}."
        )
        for field, value in data.items():
            if field == "avatar":
                assert response.data.get("avatar").startswith(
                    "http"
                ), "Неверно сохраняется поле avatar в профиле клиента."
            else:
                assert (
                    response.data.get(field) == value
                ), f"При изменении профиля клиента поле {field} не изменилось."

    def test_04_access_to_client_profile(self, client_client, guest_client):
        """Профиль клиента в ЛК доступен только клиенту."""
        scenarios = (
            ("Клиент", client_client, HTTPStatus.OK),
            ("Гость", guest_client, HTTPStatus.UNAUTHORIZED),
            # добавить психолога, когда будет фикстура
        )
        for name, client, status in scenarios:
            response = client.get(self.profile_url)
            assert response.status_code == status, (
                "Ошибка доступа к личному кабинету клиента при попытке зайти"
                f'пользователем "{name}" получен ответ {response.status_code}'
            )
