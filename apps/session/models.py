from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

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
    is_free = models.BooleanField(
        verbose_name='Свободно',
        default=True
    )

    @property
    def datetime_to(self):
        return self.datetime_from + timedelta(hours=1)

    class Meta:
        verbose_name = 'Окно записи'
        verbose_name_plural = 'Окна записи'
        constraints = [
            models.UniqueConstraint(
                fields=['psychologist', 'datetime_from'],
                name='unique_slots'
            ),
        ]

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
