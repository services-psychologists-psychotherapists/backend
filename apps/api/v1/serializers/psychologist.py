from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method

from apps.api.v1.serializers.fields import ImageFieldSerialiser
from apps.api.v1.validators import validate_file_size
from apps.core.models import Gender
from apps.core.constants import MIN_PRICE, MAX_PRICE, SESSION_DURATION
from apps.psychologists.models import Institute
from apps.psychologists.selectors import (get_education, get_service,
                                          get_free_slots)
from apps.psychologists.validators import (
    validate_birthday as _validate_birthday,
    validate_graduation_year as _validate_graduation_year,
)
from apps.users.models import CustomUser
from apps.session.models import Slot


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'email')
        model = CustomUser


class CommonInfoSerializer(serializers.Serializer):
    """
    Сериализатор для Theme, Approach
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)


class InstituteSerializer(CommonInfoSerializer):
    """
    Сериализатор для Institute
    """
    is_higher = serializers.BooleanField(read_only=True)


class SlotPsychoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для слотов
    """
    datetime_from = serializers.DateTimeField()

    class Meta:
        fields = ('id', 'datetime_from')
        model = Slot


class PsychoEducationShortSerializer(serializers.ModelSerializer):
    speciality = serializers.CharField(max_length=50)
    graduation_year = serializers.CharField(max_length=10)

    class Meta:
        fields = ('title', 'speciality', 'graduation_year')
        model = Institute


class PsychoEducationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    speciality = serializers.CharField(max_length=50)
    graduation_year = serializers.CharField(max_length=10)
    document = ImageFieldSerialiser()

    class Meta:
        fields = ('title', 'speciality', 'graduation_year', 'document')
        model = Institute
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'title': 'PsychoEducationSerializer',
            'properties': {
                'title': openapi.Schema(
                    title='title',
                    type=openapi.TYPE_STRING,
                    max_length=200,
                ),
                'speciality': openapi.Schema(
                    title='speciality',
                    type=openapi.TYPE_STRING,
                    max_length=50,
                ),
                'graduation_year': openapi.Schema(
                    title='graduation_year',
                    type=openapi.TYPE_STRING,
                    max_length=10,
                ),
                'document': openapi.Schema(
                    title='document',
                    type=openapi.TYPE_STRING,
                    description='Картинка в base64',
                ),
            },
            "required": ['title', 'speciality', 'graduation_year'],
         }

    def validate_document(self, value):
        validate_file_size(value)
        return value

    def validate_graduation_year(self, value):
        try:
            _validate_graduation_year(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


class CreatePsychologistSerializer(serializers.Serializer):
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
    institutes = PsychoEducationSerializer(many=True)
    courses = PsychoEducationSerializer(many=True, required=False)

    def validate_price(self, value):
        if value < MIN_PRICE or value > MAX_PRICE:
            raise serializers.ValidationError(
                'Введите корректную цену на услугу'
            )
        return value

    def validate_birthday(self, value):
        try:
            _validate_birthday(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value


class UpdatePsychologistSerializer(CreatePsychologistSerializer):
    experience = None


class CommonPsychologistSerializer(serializers.Serializer):
    """
    Общие данные для сериализаторов на выдачу
    """
    id = serializers.UUIDField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    about = serializers.CharField(max_length=500)
    price = serializers.SerializerMethodField()
    avatar = ImageFieldSerialiser()
    experience = serializers.IntegerField()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_price(self, obj):
        service = get_service(obj)
        return service.price


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
        serializer_or_field=PsychoEducationSerializer(many=True)
    )
    def get_institutes(self, obj):
        institutes = get_education(obj, True)
        serializer = PsychoEducationSerializer(
            institutes,
            many=True,
            context={'request': self.context.get('request'),
                     'view': self.context.get('view')},
        )
        return serializer.data

    @swagger_serializer_method(
        serializer_or_field=PsychoEducationSerializer(many=True)
    )
    def get_courses(self, obj):
        courses = get_education(obj, False)
        serializer = PsychoEducationSerializer(
            courses,
            many=True,
            context={'request': self.context.get('request'),
                     'view': self.context.get('view')},
        )
        return serializer.data


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
    age = serializers.IntegerField()
    speciality = serializers.CharField()
    themes = CommonInfoSerializer(many=True)
    approaches = CommonInfoSerializer(many=True)
    institutes = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    @swagger_serializer_method(
        serializer_or_field=PsychoEducationShortSerializer(many=True)
    )
    def get_institutes(self, obj):
        institutes = get_education(obj, True)
        serializer = PsychoEducationShortSerializer(
            institutes,
            many=True,
        )
        return serializer.data

    @swagger_serializer_method(
        serializer_or_field=PsychoEducationShortSerializer(many=True)
    )
    def get_courses(self, obj):
        courses = get_education(obj, False)
        serializer = PsychoEducationShortSerializer(
            courses,
            many=True,
        )
        return serializer.data
