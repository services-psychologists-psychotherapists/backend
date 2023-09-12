from django.utils import timezone
from rest_framework import serializers

from apps.api.v1.serializers.fields import ImageFieldSerialiser
from apps.api.v1.validators import validate_file_size
from apps.core.models import Gender
from apps.core.constants import MIN_PRICE, MAX_PRICE
from apps.psychologists import models
from apps.users.models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'email')
        model = CustomUser


class CommonInfoSerializer(serializers.Serializer):
    """
    Input сериализатор для Theme, Approach
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institute
        fields = ('id', 'title', 'is_higher')
        read_only_fields = ('is_higher', )


class PsychoEducationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    speciality = serializers.CharField(max_length=50)
    graduation_year = serializers.CharField(max_length=10)
    document = ImageFieldSerialiser()

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
    birthdate = serializers.DateField(input_formats=["%d.%m.%Y", ])  # format="%d.%m.%Y" # noqa E501
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

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['gender'] = instance.get_gender_display()
    #     rep['birthdate'] = instance.birthdate.strftime("%d.%m.%Y")
    #     return rep
