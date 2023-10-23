from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.clients.models import Client
from apps.core.constants import SESSION_DURATION
from apps.psychologists.models import ProfilePsychologist


class Slot(models.Model):
    """Окно записи"""

    psychologist = models.ForeignKey(
        ProfilePsychologist,
        on_delete=models.CASCADE,
        related_name="slots",
        verbose_name="Специалист",
    )
    datetime_from = models.DateTimeField(
        verbose_name="Начало сессии", db_index=True
    )
    datetime_to = models.DateTimeField(
        verbose_name="Окончание сессии",
        blank=True,
    )
    is_free = models.BooleanField(
        verbose_name="Свободно",
        default=True,
    )

    @property
    def date(self):
        return timezone.localdate(self.datetime_from).strftime("%d.%m.%Y")

    class Meta:
        ordering = ("datetime_from",)
        verbose_name = "Окно записи"
        verbose_name_plural = "Окна записи"
        constraints = [
            models.UniqueConstraint(
                fields=["psychologist", "datetime_from"], name="unique_slots"
            ),
        ]

    def __str__(self):
        return (
            f"{self.psychologist}: {self.datetime_from} "
            f"{self.datetime_to} - {self.is_free}"
        )

    def save(self, *args, **kwargs):
        self.datetime_to = self.datetime_from + timedelta(
            minutes=SESSION_DURATION
        )
        super().save(*args, **kwargs)


class Session(models.Model):
    """Сессия"""

    class Type(models.TextChoices):
        """Тип сессии"""

        PERSONAL = "personal", "персональная"
        GROUP = "group", "групповая"

    class Format(models.TextChoices):
        """Формат сессии"""

        ONLINE = "online", "онлайн"
        OFFLINE = "offline", "личная встреча"

    class Status(models.TextChoices):
        """Статус оплаты сессии."""

        PAID = "paid", "Оплачена"
        UNPAID = "unpaid", "Требуется оплата"

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="sessions"
    )
    slot = models.OneToOneField(
        Slot,
        on_delete=models.CASCADE,
        verbose_name="Окно записи",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PAID,
        verbose_name="Статус оплаты",
    )
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.PERSONAL,
        verbose_name="Тип сессии",
    )
    price = models.PositiveIntegerField(verbose_name="Стоимость сессии")
    format = models.CharField(
        max_length=10,
        choices=Format.choices,
        default=Format.ONLINE,
        verbose_name="Формат сессии",
    )
    client_link = models.TextField(
        verbose_name="Ссылка для клиента",
        null=True,
    )
    psycho_link = models.TextField(
        verbose_name="Ссылка для психолога",
        null=True,
    )

    class Meta:
        verbose_name = "Сессия"
        verbose_name_plural = "Сессии"

    def __str__(self):
        return f"{self.client}: {self.slot} - {self.status}"
