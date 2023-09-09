import uuid
from django.db import models
from django.conf import settings

from .validators import validate_birthday


class Gender(models.TextChoices):
    """Пол человека на выбор."""
    MALE = 'male', 'мужской'
    FEMALE = 'female', 'женский'
    OTHER = 'other', 'другой'


class Client(models.Model):
    """Модель описывает Профиль Клиента."""
    id = models.UUIDField(
        verbose_name='Уникальный id',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client',
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        blank=True,
    )
    gender = models.CharField(
        verbose_name='Пол',
        max_length=15,
        choices=Gender.choices,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True,
        validators=[validate_birthday],
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=12,
        blank=True,
    )

    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиента'

    def __str__(self):
        return f'Профиль клиента пользователя {self.user}'
