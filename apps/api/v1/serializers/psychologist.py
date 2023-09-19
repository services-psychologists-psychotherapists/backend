from django.utils import timezone
from rest_framework import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method

from apps.api.v1.serializers.fields import ImageFieldSerialiser
from apps.api.v1.validators import validate_file_size
from apps.core.models import Gender
from apps.core.constants import (MIN_PRICE, MAX_PRICE, MAX_LIFESPAN,
                                 PSYCHO_MIN_AGE)
from apps.psychologists.selectors import get_education
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
        finish_year = int(value.split('-')[-1])
        cur_year = timezone.now().year
        if finish_year > cur_year:
            raise serializers.ValidationError(
                'Укажите корректный год окончания обучения'
            )
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
        cur = timezone.now()
        age = cur.year - value.year
        if (cur.month, cur.day) < (value.month, value.day):
            return age - 1
        if age > MAX_LIFESPAN:
            raise serializers.ValidationError(
                'Укажите корректный год рождения'
            )
        if age < PSYCHO_MIN_AGE:
            raise serializers.ValidationError(
                'Мы работаем с психологами старше 25 лет'
            )
        return value


class UpdatePsychologistSerializer(CreatePsychologistSerializer):
    experience = None


class PsychologistSerializer(CreatePsychologistSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    password = serializers.CharField(source='user.password', read_only=True)  # TODO: Не знаю как правильно сериализовать. # noqa E501
    avatar = ImageFieldSerialiser()
    institutes = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    @swagger_serializer_method(
        serializer_or_field=PsychoEducationSerializer(many=True)
    )
    def get_institutes(self, obj):
        institutes = get_education(obj, True)
        serializer = PsychoEducationSerializer(institutes,
                                               many=True)
        return serializer.data

    @swagger_serializer_method(
        serializer_or_field=PsychoEducationSerializer(many=True)
    )
    def get_courses(self, obj):
        courses = get_education(obj, False)
        serializer = PsychoEducationSerializer(courses,
                                               many=True)
        return serializer.data

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_price(self, obj):
        """
        Сделано с учетом того, что сейчас возможна только 1
        цена на все и один формат
        """
        service = obj.services.all()[0]
        if service:
            return service.price
        return 1
