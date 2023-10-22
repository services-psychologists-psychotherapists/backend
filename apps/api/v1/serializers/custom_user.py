from rest_framework import serializers

from apps.users.models import CustomUser


class CustomUserMeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["name", "is_psychologists", "is_client", "email"]

    def get_name(self, obj):
        if obj.is_psychologists:
            return obj.psychologists.first_name
        elif obj.is_client:
            return obj.client.first_name
        return ""
