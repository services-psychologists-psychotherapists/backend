from django.db.transaction import atomic
from django.http import HttpRequest

from apps.users.models import CustomUser

from .models import Client
from .threads import ClientActivationEmailThread


def parse_data(data: dict) -> tuple[dict, dict]:
    """
    Делит валидированные регистрационные данные клиента
    на пользовательские и данные профиля.
    """
    client_args = ('first_name', 'birthday', 'phone_number')
    user_data = data.get('user')
    client_data = {key: data[key] for key in client_args if key in data}
    return user_data, client_data


@atomic
def create_client(
    data: dict, request: HttpRequest
) -> tuple[CustomUser, Client]:
    """
    Создание пользователя, создание клиента, отправка письма клиенту со ссылкой
    для подтверждения почты и активации аккаунта.
    """
    user_data, client_data = parse_data(data)
    user = CustomUser.objects.create_user(**user_data)
    client = Client.objects.create(user=user, **client_data)

    ClientActivationEmailThread(request, user).start()

    return client
