from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from apps.session.models import Session, Slot
from apps.session.services import create_session
from apps.clients.models import Client


class ShortClientSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для полей Клиента."""

    class Meta:
        fields = ("id", "first_name", "last_name", "avatar")
        model = Client


class SlotSerializer(serializers.ModelSerializer):
    """Сериализация полей Слота для создания и чтения."""

    client = ShortClientSerializer(source="session.client", required=False)
    href = serializers.URLField(source="session.psycho_link", required=False)
    session_id = serializers.IntegerField(source="session.id", required=False)

    class Meta:
        fields = (
            "id",
            "date",
            "datetime_from",
            "datetime_to",
            "is_free",
            "client",
            "href",
            "session_id",
        )
        model = Slot
        read_only_fields = (
            "date",
            "datetime_to",
            "client",
            "is_free",
            "href",
            "session_id",
        )

    def validate_datetime_from(self, start_time):
        user = self.context["request"].user
        up_limit = start_time.replace(hour=start_time.hour + 1)
        low_limit = start_time.replace(hour=start_time.hour - 1)
        if Slot.objects.filter(
            Q(datetime_from__lt=up_limit) & Q(datetime_from__gt=low_limit),
            psychologist__user=user,
        ).exists():
            raise serializers.ValidationError(
                "Окно записи пересекается с другими окнами специалиста."
            )
        if start_time < timezone.now():
            raise serializers.ValidationError(
                "Время начала сессии не может быть меньше текущего времени."
            )

        return super().validate(start_time)


class CreateSessionSerializer(serializers.ModelSerializer):
    """Сериализация данных при создании сессии."""

    class Meta:
        fields = ("id", "slot")
        model = Session

    def create(self, validated_data):
        request = self.context.get("request")
        return create_session(request, validated_data.get("slot"))

    def validate_slot(self, slot):
        if slot.datetime_from < timezone.now():
            raise serializers.ValidationError(
                "Вы не можете запланировать сессию на прошедшее время."
            )
        return slot

    def validate(self, attrs):
        user = self.context.get("request").user
        if user.client.sessions.filter(
            slot__datetime_from__gte=timezone.now()
        ).exists():
            raise serializers.ValidationError(
                "Вы можете иметь только 1 запланированную сессию."
            )
        return super().validate(attrs)
