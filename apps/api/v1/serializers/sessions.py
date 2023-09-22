from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from apps.session.models import Slot
from apps.clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'avatar')
        model = Client


class SlotSerializer(serializers.ModelSerializer):
    client = ClientSerializer(source='session.client', required=False)
    href = serializers.URLField(source='session.psycho_link', required=False)

    class Meta:
        fields = ('id', 'date', 'datetime_from', 'datetime_to', 'is_free', 'client', 'href')
        model = Slot
        read_only_fields = ('datetime_to', 'session', 'client', 'href')

    def validate_datetime_from(self, start_time):
        user = self.context['request'].user
        up_limit = start_time.replace(hour=start_time.hour+1)
        low_limit = start_time.replace(hour=start_time.hour-1)
        if Slot.objects.filter(
            Q(datetime_from__lt=up_limit) & Q(datetime_from__gt=low_limit),
            psychologist__user=user,
        ).exists():
            raise serializers.ValidationError(
                'Окно записи пересекается с другими окнами специалиста.'
            )

        if start_time < timezone.now():
            raise serializers.ValidationError(
                'Время начала сессии не может быть меньше текущего времени.'
            )

        return super().validate(start_time)


class FreeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'datetime_from', 'date')
        model = Slot
