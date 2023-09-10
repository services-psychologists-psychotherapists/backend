from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from apps.psychologists.models import ProfilePsychologist, Theme, Service
from apps.clients.models import Client


class Slot(models.Model):
    """Окно записи"""
    psychologist = models.ForeignKey(
        ProfilePsychologist,
        on_delete=models.CASCADE,
        related_name='slots',
        verbose_name='Специалист'
    )
    datetime_from = models.DateTimeField(
    )
    datetime_to = models.DateTimeField(
    )
    is_free = models.BooleanField(
        verbose_name='Свободно',
        default=True
    )

    class Meta:
        verbose_name = 'Окно записи'
        verbose_name_plural = 'Окна записи'
        constraints = [
            models.UniqueConstraint(
                fields=['psychologist', 'datetime_from', 'datetime_to'],
                name='unique_slots'
            ),
        ]

    def clean(self):
        if self.datetime_from > self.datetime_to:
            raise ValidationError(
                {'datetime_to': ('Значение должно быть больше'
                                 ', чем datetime_from')}
            )
        elif self.datetime_to - self.datetime_from != timedelta(hours=1):
            raise ValidationError(
                {'datetime_to': ('Значение должно быть больше '
                                 'daterime_from ровно на 1 час')}
            )

    def __str__(self):
        return (f'{self.psychologist}: {self.datetime_from} '
                f'{self.datetime_to} - {self.is_free}')


class Session(models.Model):
    """Сессия"""
    class StatusChoice(models.TextChoices):
        PAID = 'P', _('Оплаченный')
        UNPAID = 'UNP', _('Неоплаченный')

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    slot = models.OneToOneField(
        Slot,
        on_delete=models.CASCADE,
        verbose_name='Окно записи'
    )
    status = models.CharField(
        max_length=3,
        choices=StatusChoice.choices,
        default=StatusChoice.UNPAID,
        verbose_name='Статус записи'
    )
    themes = models.ManyToManyField(
        Theme,
        verbose_name='Тема сессии'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def __str__(self):
        return f'{self.client}: {self.slot} - {self.status}'
