from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from ..permissions import IsClientOnly
from ..serializers.clients import (ClientSerializer, CreateClientSerializer,
                                   UserSerializer)


@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: UserSerializer, 400: 'Bad request'}
))
class CreateClientView(generics.CreateAPIView):
    """Создание пользователя-клиента и профиля клиента."""
    serializer_class = CreateClientSerializer
    permission_classes = (AllowAny,)


class ClientView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и изменение профиля клиента.
    Поле "avatar" передается в формате base64.
    """
    serializer_class = ClientSerializer
    permission_classes = (IsClientOnly,)
    http_method_names = ['get', 'put']

    def get_object(self):
        return self.request.user.client
