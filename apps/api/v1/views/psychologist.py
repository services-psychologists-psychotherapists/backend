from rest_framework import filters, viewsets, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.api.v1.serializers import psychologist as psycho
from apps.psychologists.services import create_psychologist
from apps.psychologists import models


class CreatePsychologistView(views.APIView):
    """Создание психолога на сайте. Доступ - любой пользователь."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Создание профиля психолога по анкете"""
        user_ser = psycho.CreateUserSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        psychologist_ser = psycho.CreatePsychologistSerializer(
            data=request.data
        )
        psychologist_ser.is_valid(raise_exception=True)
        user, _ = create_psychologist(user_ser.validated_data,
                                      psychologist_ser.validated_data,
                                      )
        return Response(psycho.CreateUserSerializer(user).data,
                        status=status.HTTP_201_CREATED)


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Theme.objects.all()
    serializer_class = psycho.ThemeSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^title', )
    permission_classes = (AllowAny,)
    pagination_class = None


class ApproacheViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Approach.objects.all()
    serializer_class = psycho.ApproachSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^title', )
    permission_classes = (AllowAny,)
    pagination_class = None


class InstituteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Institute.objects.all()
    serializer_class = psycho.InstituteSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('is_higher', )
    search_fields = ('^title', )
    pagination_class = None
