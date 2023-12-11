from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method

from apps.api.v1.serializers.fields import ImageFieldSerialiser
from apps.api.v1.validators import validate_file_size, validate_file_ext
from apps.core.models import Gender, UploadFile
from apps.core.constants import MIN_PRICE, MAX_PRICE, SESSION_DURATION
from apps.psychologists.models import PsychoEducation
from apps.psychologists.selectors import (
    get_education,
    get_price,
    get_free_slots,
)
from apps.psychologists.validators import (
    validate_birthday as _validate_birthday,
    validate_graduation_year as _validate_graduation_year,
)
from apps.users.models import CustomUser
from apps.session.models import Slot


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "email")
        model = CustomUser


class CommonInfoSerializer(serializers.Serializer):
    """Сериализатор для Theme, Approach."""

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)


class InstituteSerializer(CommonInfoSerializer):
    """Сериализатор для Institute."""

    is_higher = serializers.BooleanField(read_only=True)


class SlotPsychoSerializer(serializers.ModelSerializer):
    """Сериализатор для слотов."""

    datetime_from = serializers.DateTimeField()

    class Meta:
        fields = ("id", "datetime_from")
        model = Slot


class UploadFileSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки документа об образовании."""

    path = serializers.FileField()

    class Meta:
        fields = ("id", "path")
        model = UploadFile

    def validate(self, attrs):
        errors = []
        try:
            validate_file_size(attrs.get("path"))
        except serializers.ValidationError as e:
            errors.extend(e.args)

        try:
            validate_file_ext(attrs.get("path"))
        except serializers.ValidationError as e:
            errors.extend(e.args)

        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)


class EducationShortOutputSerializer(serializers.ModelSerializer):
    """Сериализатор на выдачу для полной карточки психолога в каталоге."""

    title = serializers.CharField(source="institute.title")
    speciality = serializers.CharField()
    graduation_year = serializers.CharField()

    class Meta:
        fields = ("title", "speciality", "graduation_year")
        model = PsychoEducation


class EducationOutputSerializer(EducationShortOutputSerializer):
    """Сериализатор на выдачу для ЛК психолога."""

    document = serializers.FileField(source="document.path")

    class Meta:
        fields = ("title", "speciality", "graduation_year", "document")
        model = PsychoEducation


class EducationInputSerializer(serializers.Serializer):
    """Сериализатор для создания и апдейта профиля психолога."""

    title = serializers.CharField(max_length=200)
    speciality = serializers.CharField(max_length=50)
    graduation_year = serializers.CharField(max_length=10)
    document = serializers.UUIDField()

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "EducationInputSerializer",
            "properties": {
                "title": openapi.Schema(
                    title="title",
                    type=openapi.TYPE_STRING,
                    max_length=200,
                ),
                "speciality": openapi.Schema(
                    title="speciality",
                    type=openapi.TYPE_STRING,
                    max_length=50,
                ),
                "graduation_year": openapi.Schema(
                    title="graduation_year",
                    type=openapi.TYPE_STRING,
                    max_length=10,
                ),
                "document": openapi.Schema(
                    title="document",
                    type=openapi.TYPE_STRING,
                ),
            },
            "required": ["title", "speciality", "graduation_year", "document"],
        }

    def validate_graduation_year(self, value):
        try:
            _validate_graduation_year(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


class CreatePsychologistSerializer(serializers.Serializer):
    """Сериализатор для создания профиля психолога."""

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthday = serializers.DateField()
    gender = serializers.ChoiceField(choices=Gender.choices)
    phone_number = serializers.CharField(max_length=12, required=False)
    experience = serializers.IntegerField()
    about = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    themes = CommonInfoSerializer(many=True)
    approaches = CommonInfoSerializer(many=True)
    institutes = EducationInputSerializer(many=True)
    courses = EducationInputSerializer(many=True, required=False)

    def validate_price(self, value):
        if value < MIN_PRICE or value > MAX_PRICE:
            raise serializers.ValidationError(
                "Введите корректную цену на услугу"
            )
        return value

    def validate_birthday(self, value):
        try:
            _validate_birthday(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


class UpdatePsychologistSerializer(CreatePsychologistSerializer):
    """Сериализатор для обновления полей профиля Психолога."""

    experience = None
    avatar = ImageFieldSerialiser()


class CommonPsychologistSerializer(serializers.Serializer):
    """Общие данные для сериализаторов на выдачу."""

    id = serializers.UUIDField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    about = serializers.CharField(max_length=500)
    price = serializers.SerializerMethodField()
    avatar = ImageFieldSerialiser()
    experience = serializers.IntegerField()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_price(self, obj):
        price = get_price(obj)
        return price


class PsychologistSerializer(CommonPsychologistSerializer):
    """
    Профиль психолога
    """

    birthday = serializers.DateField()
    gender = serializers.ChoiceField(choices=Gender.choices)
    phone_number = serializers.CharField(max_length=12, required=False)
    themes = CommonInfoSerializer(many=True)
    approaches = CommonInfoSerializer(many=True)
    institutes = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    @swagger_serializer_method(
        serializer_or_field=EducationOutputSerializer(many=True)
    )
    def get_institutes(self, obj):
        institutes = get_education(obj, True)
        serializer = EducationOutputSerializer(
            institutes,
            many=True,
            context={
                "request": self.context.get("request"),
                "view": self.context.get("view"),
            },
        )
        return serializer.data

    @swagger_serializer_method(
        serializer_or_field=EducationOutputSerializer(many=True)
    )
    def get_courses(self, obj):
        courses = get_education(obj, False)
        serializer = EducationOutputSerializer(
            courses,
            many=True,
            context={
                "request": self.context.get("request"),
                "view": self.context.get("view"),
            },
        )
        return serializer.data


class SuperShortPsychoSerializer(CommonPsychologistSerializer):
    """
    Данные психолога для страницы создания сессии.
    """

    speciality = serializers.CharField()
    duration = serializers.SerializerMethodField()
    format = serializers.SerializerMethodField()

    def get_duration(self, obj) -> int:
        return SESSION_DURATION

    def get_format(self, obj) -> str:
        return "онлайн"


class ShortPsychoCardSerializer(CommonPsychologistSerializer):
    """
    Данные для краткой карточки психолога
    """

    duration = serializers.SerializerMethodField()
    slots = serializers.SerializerMethodField()

    def get_duration(self, obj) -> int:
        return SESSION_DURATION

    @swagger_serializer_method(
        serializer_or_field=SlotPsychoSerializer(many=True)
    )
    def get_slots(self, obj):
        slots = get_free_slots(obj)
        serializer = SlotPsychoSerializer(slots, many=True)
        return serializer.data


class FullPsychoCardSerializer(ShortPsychoCardSerializer):
    """
    Данные для полной карточки психолога
    """

    age = serializers.IntegerField()
    speciality = serializers.CharField()
    themes = CommonInfoSerializer(many=True)
    approaches = CommonInfoSerializer(many=True)
    institutes = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    @swagger_serializer_method(
        serializer_or_field=EducationShortOutputSerializer(many=True)
    )
    def get_institutes(self, obj):
        institutes = get_education(obj, True)
        serializer = EducationShortOutputSerializer(
            institutes,
            many=True,
        )
        return serializer.data

    @swagger_serializer_method(
        serializer_or_field=EducationShortOutputSerializer(many=True)
    )
    def get_courses(self, obj):
        courses = get_education(obj, False)
        serializer = EducationShortOutputSerializer(
            courses,
            many=True,
        )
        return serializer.data
