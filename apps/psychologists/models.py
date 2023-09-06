import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Institute(models.Model):
    """Институт"""
    title = models.CharField(
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Институт'
        verbose_name_plural = 'Институты'

    def __str__(self):
        return f'{self.title}'


class Theme(models.Model):
    """Темы, с которыми работает психолог"""
    title = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return f'{self.title}'


class Approach(models.Model):
    """Подход, используемый психологом в работе"""
    title = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = 'Подход'
        verbose_name_plural = 'Подходы'

    def __str__(self):
        return f'{self.title}'


class ProfilePsychologist(models.Model):
    """Профиль психолога"""

    class Gender(models.TextChoices):
        MALE = 'M', _('MALE')
        FEMALE = 'F', _('FEMALE')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        max_length=50,
    )
    middle_name = models.CharField(
        max_length=50,
    )
    last_name = models.CharField(
        max_length=50,
    )
    birthdate = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
    )
    phone_number = models.CharField(
        max_length=12,
        blank=True,
        default='',
    )
    started_working = models.DateField()
    education = models.ManyToManyField(
        Institute,
        through='PsychoEducation',
    )
    themes = models.ManyToManyField(
        Theme,
    )
    approaches = models.ManyToManyField(
        Approach,
    )
    about = models.TextField(
        max_length=500,
    )
    avatar = models.ImageField(
        upload_to=user_directory_path,
    )
    is_verified = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Профиль психолога'
        verbose_name_plural = 'Профили психолога'

    @property
    def age(self):
        cur = timezone.now()
        age = cur.year - self.birthdate.year
        if (cur.month, cur.day) < (self.birthdate.month, self.birthdate.day):
            return age - 1
        return age

    @property
    def experience(self):
        today = timezone.now()
        return today.year - self.started_working.year

    def __str__(self):
        return f'{self.first_name} {self.last_name[0]}'

    def clean_fields(self, exclude=None):
        max_lifespan = 120
        cur_year = timezone.now().year
        min_age = 25
        if self.birthdate.year < cur_year - max_lifespan:
            raise ValidationError(
                {'birthdate': 'Укажите корректный год рождения'}
            )
        if self.age < min_age:
            raise ValidationError(
                {'birthdate': 'Мы работаем с психологами старше 25 лет'}
            )
        super().clean_fields(exclude=exclude)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PsychoEducation(models.Model):
    """Образование психолога"""
    psychologist = models.ForeignKey(
        ProfilePsychologist,
        on_delete=models.CASCADE,
    )
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
    )
    graduation_year = models.DateField()
    document = models.FileField(
        upload_to=user_directory_path,
    )

    class Meta:
        verbose_name = 'Образование психолога'

    def __str__(self):
        return f'{self.psychologist}: {self.institute}'


class Service(models.Model):

    class Type(models.TextChoices):
        PERSONAL = 'P', _('PERSONAL')
        GROUP = 'G', _('GROUP')

    class Format(models.TextChoices):
        ONLINE = 'ON', 'ONLINE'
        OFFLINE = 'OF', 'OFFLINE'

    psychologist = models.ForeignKey(
        ProfilePsychologist,
        on_delete=models.CASCADE,
        related_name='services',
    )
    type = models.CharField(
        max_length=1,
        choices=Type.choices,
    )
    price = models.PositiveIntegerField()
    duration = models.PositiveSmallIntegerField()
    format = models.CharField(
        max_length=2,
        choices=Format.choices,
        default=Format.ONLINE,
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.psychologist}: {self.type} {self.price}'
