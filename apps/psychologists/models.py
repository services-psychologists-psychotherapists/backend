import uuid

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.core.constants import MIN_PRICE, MAX_PRICE, SESSION_DURATION
from apps.core.models import Gender, UploadFile
from apps.psychologists.validators import (
    validate_birthday,
    validate_graduation_year,
    validate_started_working,
)


def user_directory_path(instance, filename):
    if isinstance(instance, ProfilePsychologist):
        return "user_{0}/{1}".format(instance.user.id, filename)
    return "user_{0}/{1}".format(instance.psychologist.user.id, filename)


class CommonInfo(models.Model):
    """
    Базовая модель для Institute, Theme, Approach
    """

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=("title",),
                name="%(app_label)s_%(class)s_index",
            ),
        ]

    def __str__(self):
        return f"{self.title}"


class Institute(CommonInfo):
    """Институт"""

    is_higher = models.BooleanField(
        verbose_name="Высшее",
    )

    class Meta(CommonInfo.Meta):
        verbose_name = "Институт"
        verbose_name_plural = "Институты"


class Theme(CommonInfo):
    """Темы, с которыми работает психолог"""

    class Meta(CommonInfo.Meta):
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Approach(CommonInfo):
    """Подход, используемый психологом в работе"""

    class Meta(CommonInfo.Meta):
        verbose_name = "Подход"
        verbose_name_plural = "Подходы"


class ProfilePsychologist(models.Model):
    """Профиль психолога"""

    id = models.UUIDField(
        verbose_name="Уникальный id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=50,
    )
    birthday = models.DateField(
        verbose_name="Дата рождения",
        validators=[validate_birthday],
    )
    gender = models.CharField(
        verbose_name="Пол",
        max_length=10,
        choices=Gender.choices,
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=12,
        blank=True,
        default="",
    )
    started_working = models.DateField(
        verbose_name="Год начала практики",
        validators=[validate_started_working],
    )
    education = models.ManyToManyField(
        Institute,
        through="PsychoEducation",
        verbose_name="Образование",
    )
    themes = models.ManyToManyField(
        Theme,
        verbose_name="Темы",
    )
    approaches = models.ManyToManyField(
        Approach,
        verbose_name="Подходы",
    )
    about = models.TextField(
        verbose_name="Обо мне",
        max_length=500,
    )
    avatar = models.ImageField(
        verbose_name="Фото",
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    speciality = models.CharField(
        verbose_name="Специальность",
        max_length=50,
        default="Психолог",
        blank=True,
    )
    is_verified = models.BooleanField(
        verbose_name="Верификация",
        default=False,
    )

    class Meta:
        verbose_name = "Профиль психолога"
        verbose_name_plural = "Профили психолога"
        default_related_name = "psychologists"

    @property
    def age(self):
        cur = timezone.now()
        age = cur.year - self.birthday.year
        if (cur.month, cur.day) < (self.birthday.month, self.birthday.day):
            return age - 1
        return age

    @property
    def experience(self):
        today = timezone.now()
        return today.year - self.started_working.year

    def get_full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def __str__(self):
        return f"{self.first_name} {self.last_name[0]}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PsychoEducation(models.Model):
    """Образование психолога"""

    psychologist = models.ForeignKey(
        ProfilePsychologist,
        on_delete=models.CASCADE,
        verbose_name="Психолог",
    )
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        verbose_name="Институт",
    )
    speciality = models.CharField(
        verbose_name="Специальность",
        max_length=50,
    )
    graduation_year = models.CharField(
        verbose_name="Даты обучения / Год выпуска",
        max_length=10,
        validators=[validate_graduation_year],
    )
    document = models.OneToOneField(
        UploadFile,
        on_delete=models.CASCADE,
        verbose_name="Документ об образовании",
    )

    class Meta:
        verbose_name = "Образование психолога"
        verbose_name_plural = "Профили психологов"
        default_related_name = "psychoeducation"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "psychologist",
                    "institute",
                    "speciality",
                    "graduation_year",
                ),
                name="unique_education",
            )
        ]

    def __str__(self):
        return f"{self.psychologist}: {self.institute}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Service(models.Model):
    class Type(models.TextChoices):
        """Тип сессии"""

        PERSONAL = "personal", "личная"
        GROUP = "group", "групповая"
        NOMATTER = "no_matter", "неважно"

    class Format(models.TextChoices):
        """Формат сессии"""

        ONLINE = "online", "онлайн"
        OFFLINE = "offline", "личная встреча"
        NOMATTER = "no_matter", "неважно"

    psychologist = models.ForeignKey(
        ProfilePsychologist,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Психолог",
    )
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.NOMATTER,
        verbose_name="Тип консультации",
    )
    price = models.PositiveIntegerField(
        validators=(
            MinValueValidator(MIN_PRICE),
            MaxValueValidator(MAX_PRICE),
        ),
        verbose_name="Цена",
    )
    duration = models.PositiveSmallIntegerField(
        default=SESSION_DURATION,
        verbose_name="Продолжительность сессии",
    )
    format = models.CharField(
        max_length=10,
        choices=Format.choices,
        default=Format.ONLINE,
        verbose_name="Формат сессии",
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.psychologist}: {self.type} {self.price}"
