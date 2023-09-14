from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from apps.clients.models import Client
from apps.users.models import CustomUser


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
    """Сериализатор для клиента, в т.ч. ЛК."""
    class Meta:
        fields = ('id', 'name', 'gender', 'birthday', 'phone_number')
        model = Client

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['gender'] = instance.get_gender_display()
        return rep
