from django.db import models


class Gender(models.TextChoices):
    """Пол человека на выбор"""

    MALE = 'male', 'мужской'
    FEMALE = 'female', 'женский'
    OTHER = 'other', 'другой'
