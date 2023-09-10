from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.clients.selectors import get_client
from apps.clients.services import create_client, update_client

from ..permissions import IsClientOnly
from ..serializers.clients import CreateUserSerializer, ClientSerializer


class CreateClientApiView(views.APIView):
    """Создание нового клиента на сайте. Доступ - любой пользователь."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Создание нового клиента на сайте."""
        user_serializer = CreateUserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        client_serializer = ClientSerializer(data=request.data)
        client_serializer.is_valid(raise_exception=True)
        client = create_client(user_serializer.validated_data,
                               client_serializer.validated_data)
        return Response(ClientSerializer(client).data,
                        status=status.HTTP_201_CREATED)


class ClientApiView(views.APIView):
    """Просмотр и изменение данных клиентского профиля пользователя."""
    permission_classes = (IsClientOnly,)

    def get(self, request):
        """Просмотр клиентского профиля."""
        client = get_client(request.user)
        return Response(ClientSerializer(client).data,
                        status=status.HTTP_200_OK)

    def put(self, request):
        """Изменение клиентского профиля."""
        client = get_client(request.user)
        serializer = ClientSerializer(client, request.data)
        serializer.is_valid(raise_exception=True)
        client = update_client(client, serializer.validated_data)
        return Response(ClientSerializer(client).data,
                        status=status.HTTP_200_OK)
