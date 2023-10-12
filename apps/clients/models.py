import uuid
from django.db import models
from django.conf import settings

from apps.core.models import Gender

from .validators import validate_birthday


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Client(models.Model):
    """Модель описывает Профиль Клиента."""

    id = models.UUIDField(
        verbose_name="Уникальный id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client",
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=50,
        blank=True,
    )
    gender = models.CharField(
        verbose_name="Пол",
        max_length=15,
        choices=Gender.choices,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name="Дата рождения",
        validators=[validate_birthday],
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=12,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name="Фото",
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профили клиента"

    def __str__(self):
        return f"Профиль клиента пользователя {self.user}"

    def get_full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
