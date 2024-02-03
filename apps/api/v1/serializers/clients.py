from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.clients.models import Client
from apps.clients.selectors import get_my_psychologist, get_next_session
from apps.clients.services import create_client
from apps.psychologists.models import ProfilePsychologist
from apps.session.models import Session
from apps.users.models import CustomUser

from .fields import ImageFieldSerialiser


class UserSerializer(serializers.ModelSerializer):
    """Сериализация полей пользователя."""

    class Meta:
        fields = ("id", "email")
        model = CustomUser


class CreateClientSerializer(serializers.ModelSerializer):
    """Сериализация полей пользователя-клиента и профиля клиента."""

    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(source="user.password")

    class Meta:
        fields = (
            "id",
            "first_name",
            "birthday",
            "phone_number",
            "email",
            "password",
        )
        model = Client
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким адресом эл.почты существует."
            )
        return value

    def validate(self, attrs):
        """Валидация пароля по списку валидаторов в settings"""
        password = attrs.get("user").get("password")
        errors = dict()

        try:
            validate_password(password=password, user=None)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def to_representation(self, instance):
        return UserSerializer(instance=instance.user).data

    def create(self, validated_data):
        return create_client(validated_data, self.context.get("request"))


class ShortPsychologistSerializer(serializers.ModelSerializer):
    """Сериализация полей профиля психолога для ближайшей сессии."""

    class Meta:
        fields = ("id", "first_name", "last_name", "avatar")
        model = ProfilePsychologist


class FullPsychologistSerializer(serializers.Serializer):
    """Сериализация полей профиля текущего психолога клиента."""

    id = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    speciality = serializers.CharField()
    avatar = ImageFieldSerialiser()
    price = serializers.IntegerField()
    duration = serializers.IntegerField()


class SessionSerializer(serializers.ModelSerializer):
    """Сериализация полей ближайшей сессии клиента в личном кабинете."""

    psychologist = ShortPsychologistSerializer(source="slot.psychologist")
    datetime_from = serializers.DateTimeField(source="slot.datetime_from")
    datetime_to = serializers.DateTimeField(source="slot.datetime_to")
    href = serializers.URLField(source="client_link")

    class Meta:
        fields = ("id", "psychologist", "datetime_from", "datetime_to", "href")
        model = Session


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля клиента в личном кабинете."""

    avatar = ImageFieldSerialiser(required=False)
    next_session = serializers.SerializerMethodField()
    my_psychologist = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "birthday",
            "phone_number",
            "avatar",
            "next_session",
            "my_psychologist",
            "gender",
        )
        model = Client

    @swagger_serializer_method(SessionSerializer)
    def get_next_session(self, client):
        session = get_next_session(client)
        return SessionSerializer(session, context=self.context).data

    @swagger_serializer_method(FullPsychologistSerializer)
    def get_my_psychologist(self, client):
        psycho = get_my_psychologist(client)
        return FullPsychologistSerializer(psycho, context=self.context).data
