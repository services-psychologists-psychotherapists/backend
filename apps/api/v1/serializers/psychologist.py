from rest_framework import serializers
from djoser.conf import settings

from apps.psychologists import models
from apps.core.models import Gender


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Theme
        fields = ('id', 'title')


class ApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Approach
        fields = ('id', 'title')


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institute
        fields = ('id', 'title')


class CreatePsychologistSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(input_formats=["%d.%m.%Y", ])  # format="%d.%m.%Y"
    gender = serializers.ChoiceField(choices=Gender.choices)
    phone_number = serializers.CharField(max_length=12, required=False)
    experience = serializers.IntegerField()
    about = serializers.CharField(max_length=500, required=False)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['gender'] = instance.get_gender_display()
        rep['birthdate'] = instance.birthdate.strftime("%d.%m.%Y")
        return rep
