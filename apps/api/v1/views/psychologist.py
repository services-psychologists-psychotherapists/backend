from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, parsers, status, views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.api.v1.filters import (
    InstituteFilter,
    PsychoFilter,
    SlotFilter,
    TitleFilter,
)
from apps.api.v1.pagination import CustomPagination
from apps.api.v1.permissions import IsPsychologistOnly
from apps.api.v1.serializers import psychologist as psycho
from apps.core.services import create_file
from apps.psychologists import models
from apps.psychologists.selectors import (
    get_all_free_slots,
    get_all_verified_psychologists,
    get_psychologist,
    get_psychologist_for_card,
    get_psychologist_with_services,
)
from apps.psychologists.services import (
    create_psychologist,
    update_psychologist,
)


class CreatePsychologistView(views.APIView):
    """Создание психолога на сайте. Доступ - любой пользователь."""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=psycho.CreatePsychologistSerializer(),
        responses={201: psycho.CreateUserSerializer()},
    )
    def post(self, request):
        """Создание профиля психолога по анкете"""
        user_ser = psycho.CreateUserSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        psychologist_ser = psycho.CreatePsychologistSerializer(
            data=request.data
        )
        psychologist_ser.is_valid(raise_exception=True)
        user, _ = create_psychologist(
            user_ser.validated_data,
            psychologist_ser.validated_data,
        )
        return Response(
            psycho.CreateUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Theme.objects.all()
    serializer_class = psycho.CommonInfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AllowAny,)
    pagination_class = None


class ApproacheViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Approach.objects.all()
    serializer_class = psycho.CommonInfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AllowAny,)
    pagination_class = None


class InstituteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Institute.objects.all()
    serializer_class = psycho.InstituteSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = InstituteFilter
    pagination_class = None


class PsychologistProfileView(views.APIView):
    """
    Отображение / редактирование профиля психолога
    """

    permission_classes = (IsPsychologistOnly,)

    @swagger_auto_schema(responses={200: psycho.PsychologistSerializer()})
    def get(self, request):
        """Отображение профиля психолога"""
        psychologist = get_psychologist(request.user)
        return Response(
            psycho.PsychologistSerializer(
                psychologist,
                context={"request": request, "view": self},
            ).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=psycho.UpdatePsychologistSerializer(),
        responses={200: psycho.PsychologistSerializer()},
        operation_description="Жду только отредактированные поля",
    )
    def patch(self, request):
        """Редактирование профиля психолога"""
        psychologist = get_psychologist(request.user)
        serializer = psycho.UpdatePsychologistSerializer(
            psychologist, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        psychologist = update_psychologist(
            psychologist, serializer.validated_data
        )
        return Response(
            psycho.PsychologistSerializer(
                psychologist, context={"request": request, "view": self}
            ).data,
            status=status.HTTP_200_OK,
        )


class PsychoListCatalogView(generics.ListAPIView):
    """
    Отображение каталога психологов
    """

    permission_classes = (AllowAny,)
    serializer_class = psycho.ShortPsychoCardSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PsychoFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        return get_all_verified_psychologists()


class PsychoCardCatalogView(views.APIView):
    """
    Отображение карточки психолога в каталоге
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={200: psycho.FullPsychoCardSerializer()})
    def get(self, request, id=None):
        psychologist = get_psychologist_for_card(id)
        return Response(
            psycho.FullPsychoCardSerializer(psychologist).data,
            status=status.HTTP_200_OK,
        )


class ShortPsychoCardCatalogView(views.APIView):
    """
    Краткая информация о психологе на странице создания сессии.
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={200: psycho.SuperShortPsychoSerializer()})
    def get(self, request, id=None):
        psychologist = get_psychologist_with_services(id)
        return Response(
            psycho.SuperShortPsychoSerializer(
                psychologist,
                context={"request": request, "view": self},
            ).data,
            status=status.HTTP_200_OK,
        )


class FreeSlotsView(generics.ListAPIView):
    """
    Список свободных слотов на странице создания сессии.
    Фильтр 'since=DD.MM.YYYY' отдает слоты в диапазоне 14 дней с даты.
    """

    permission_classes = (AllowAny,)
    serializer_class = psycho.SlotPsychoSerializer
    filterset_class = SlotFilter

    def get_queryset(self):
        return get_all_free_slots(self.kwargs.get("id"))


class UploadFileView(views.APIView):
    """
    Загрузка документа об оброазовании
    """

    permission_classes = (AllowAny,)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    @swagger_auto_schema(
        request_body=psycho.UploadFileSerializer(),
        responses={201: psycho.UploadFileSerializer()},
    )
    def post(self, request):
        file_ser = psycho.UploadFileSerializer(data=request.FILES)
        file_ser.is_valid(raise_exception=True)
        file = create_file(file_ser.validated_data)
        return Response(
            psycho.UploadFileSerializer(file).data,
            status=status.HTTP_201_CREATED,
        )
