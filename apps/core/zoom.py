import requests
from datetime import datetime

from django.conf import settings
from rest_framework.exceptions import APIException

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

    if response.status_code != 200:
        raise APIException("Нет доступа к API Zoom.")

    response_data = response.json()
    return response_data["access_token"]


def create_meeting(topic: str, start_time: datetime,
                   duration: int = 50) -> tuple[str, str]:
    """Создание встречи Zoom. Возвращает 2 ссылки: для клиента и психолога."""
    access_token = get_token()

    headers = {
        "Authorization": f"Bearer {access_token}1",
        "Content-Type": "application/json"
    }

    payload = {
        "topic": topic,
        "duration": duration,
        'start_time': start_time.strftime('%Y-%m-%dT%H:%M:00'),
        "timezone": "Europe/Moscow",
        "type": 2,
    }

    response = requests.post(
        url=f"{API_BASE_URL}/users/me/meetings",
        headers=headers,
        json=payload,
    )

    if response.status_code != 201:
        raise APIException('Zoom не смог сформировать ссылку на встречу')

    response_data = response.json()

    client_url = response_data["join_url"]
    psychologist_url = response_data["start_url"]
    return client_url, psychologist_url
