from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.api.v1.serializers.psychologist import (CreateUserSerializer,
                                                  CreatePsychologistSerializer)
from apps.psychologists.services import create_psychologist


class CreatePsychologistView(views.APIView):
    """Создание психолога на сайте. Доступ - любой пользователь."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Создание нового клиента на сайте."""
        user_ser = CreateUserSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        psychologist_ser = CreatePsychologistSerializer(data=request.data)
        psychologist_ser.is_valid(raise_exception=True)
        psychologist = create_psychologist(user_ser.validated_data,
                                           psychologist_ser.validated_data)
        return Response(status=status.HTTP_201_CREATED)
