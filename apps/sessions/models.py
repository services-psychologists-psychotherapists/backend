from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from psychologists.models import ProfilePsychologist, Theme, Service
from clients.models import ProfileClient


class Slot(models.Model):
    """Окно записи"""
    psychologist = models.ForeignKey(
        ProfilePsychologist,
        on_delete=models.CASCADE,
        related_name='slots',
        verbose_name='Специалист'
    )
    datetime_from = models.DateTimeField(
        unique=True
    )
    datetime_to = models.DateTimeField(
        unique=True
    )
    is_free = models.BooleanField(
        verbose_name='Свободно',
        default=True
    )

    class Meta:
        verbose_name = 'Окно записи'
        verbose_name_plural = 'Окна записи'

    def clean(self):
        if self.datetime_from > self.datetime_to:
            raise ValidationError(
                {'datetime_to': ('Значение должно быть больше'
                                 ', чем datetime_from')}
            )
        elif self.datetime_to - self.datetime_from != timedelta(hour=1):
            raise ValidationError(
                {'datetime_to': ('Значение должно быть больше '
                                 'daterime_from ровно на 1 час')}
            )

    def __str__(self):
        return (f'{self.psychologist}: {self.datetime_from} '
                f'{self.datetime_to} - {self.is_free}')


class Session(models.Model):
    """Сессия"""
    class Status(models.TextChoices):
        CONFIRMED = 'C', _('Подтверждено')
        NOT_CONFIRMED = 'NC', _('Не подтверждено')

    client = models.ForeignKey(
        ProfileClient,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    slot = models.OneToOneField(
        Slot,
        on_delete=models.CASCADE,
        verbose_name='Окно записи'
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
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
