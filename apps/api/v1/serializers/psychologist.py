from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method

from apps.api.v1.serializers.fields import ImageFieldSerialiser
from apps.api.v1.validators import validate_file_size
from apps.core.models import Gender
from apps.core.constants import MIN_PRICE, MAX_PRICE
from apps.psychologists.selectors import get_education, get_service
from apps.psychologists.validators import (
    validate_birthday as _validate_birthday,
    validate_graduation_year as _validate_graduation_year,
)
from apps.users.models import CustomUser


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


class PsychoEducationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    speciality = serializers.CharField(max_length=50)
    graduation_year = serializers.CharField(max_length=10)
    document = ImageFieldSerialiser()

    class Meta:
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
            "required": ['title', 'speciality', 'graduation_year', 'document'],
         }

    def validate_graduation_year(self, value):
        try:
            _validate_graduation_year(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate_document(self, value):
        validate_file_size(value)
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


class PsychologistSerializer(CreatePsychologistSerializer):
    id = serializers.UUIDField()
    avatar = ImageFieldSerialiser()
    institutes = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

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

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_price(self, obj):
        service = get_service(obj)
        return service.price
