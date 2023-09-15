from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from apps.clients.models import Client
from apps.users.models import CustomUser

from .fields import ImageFieldSerialiser


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя-клиента."""
    class Meta:
        fields = ('id', 'email', 'password')
        model = CustomUser
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        user = CustomUser(**attrs)
        password = attrs.get("password")
        errors = dict()

        try:
            validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля клиента, в т.ч. ЛК."""
    avatar = ImageFieldSerialiser(required=False)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'birthday', 'phone_number',
                  'avatar')
        model = Client
