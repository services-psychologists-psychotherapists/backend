from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.api.v1.serializers.fields import ImageFieldSerialiser
from apps.core.models import Gender
from apps.core.constants import MIN_PRICE, MAX_PRICE
from apps.psychologists import models
from apps.users.models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'email')
        model = CustomUser


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Theme
        fields = ('id', 'title')

    def to_internal_value(self, data):
        theme = get_object_or_404(models.Theme, id=data)
        return theme


class ApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Approach
        fields = ('id', 'title')

    def to_internal_value(self, data):
        approach = get_object_or_404(models.Approach, id=data)
        return approach


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institute
        fields = ('id', 'title', 'is_higher')
        read_only_fields = ('is_higher', )


class PsychoEducationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    speciality = serializers.CharField(max_length=50)
    graduation_year = serializers.CharField(max_length=10)
    file = ImageFieldSerialiser(required=False)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ('all')


class CreatePsychologistSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(input_formats=["%d.%m.%Y", ])  # format="%d.%m.%Y" # noqa E501
    gender = serializers.ChoiceField(choices=Gender.choices)
    phone_number = serializers.CharField(max_length=12, required=False)
    experience = serializers.IntegerField()
    about = serializers.CharField(max_length=500, required=False)
    price = serializers.IntegerField()
    themes = ThemeSerializer(many=True)
    approaches = ApproachSerializer(many=True)
    institutes = PsychoEducationSerializer(many=True)
    courses = PsychoEducationSerializer(many=True)

    def validate_price(self, value):
        if value < MIN_PRICE or value > MAX_PRICE:
            raise serializers.ValidationError(
                'Введите корректную цену на услугу'
            )
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['gender'] = instance.get_gender_display()
        rep['birthdate'] = instance.birthdate.strftime("%d.%m.%Y")
        return rep
