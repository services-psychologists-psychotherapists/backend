import uuid

from django.db import models


class Gender(models.TextChoices):
    """Пол человека на выбор"""

    MALE = 'male', 'мужской'
    FEMALE = 'female', 'женский'
    OTHER = 'other', 'другой'


class UploadFile(models.Model):
    """
    Модель для загрузки документа об образовании
    """
    id = models.UUIDField(
        verbose_name='Уникальный id',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    path = models.FileField(
        verbose_name='Документ об образовании',
        upload_to='uploads/',
    )
