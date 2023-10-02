import requests
from http import HTTPStatus
from datetime import datetime

from django.conf import settings
from rest_framework.exceptions import APIException

from apps.core.constants import SESSION_DURATION

AUTH_TOKEN_URL = "https://zoom.us/oauth/token"
API_BASE_URL = "https://api.zoom.us/v2"


def get_token() -> str:
    """Получение zoom-токена."""
    data = {
        "grant_type": "account_credentials",
        "account_id": settings.ZOOM_ACCOUNT_ID,
        "client_secret": settings.ZOOM_CLIENT_SECRET,
    }
    response = requests.post(
        url=AUTH_TOKEN_URL,
        auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET),
        data=data
    )

    if response.status_code != HTTPStatus.OK:
        raise APIException("Нет доступа к API Zoom.")

    response_data = response.json()
    return response_data["access_token"]


def create_meeting(start_time: datetime,
                   duration: int = SESSION_DURATION) -> tuple[str, str]:
    """Создание встречи Zoom. Возвращает 2 ссылки: для клиента и психолога."""
    access_token = get_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "topic": 'Сеанс психолога',
        "duration": duration,
        'start_time': start_time.strftime('%Y-%m-%dT%H:%M:00Z'),
        "type": 2,
    }

    response = requests.post(
        url=f"{API_BASE_URL}/users/me/meetings",
        headers=headers,
        json=payload,
    )

    if response.status_code != HTTPStatus.CREATED:
        raise APIException('Zoom не смог сформировать ссылку на встречу')

    response_data = response.json()

    client_url = response_data["join_url"]
    psychologist_url = response_data["start_url"]
    return client_url, psychologist_url
