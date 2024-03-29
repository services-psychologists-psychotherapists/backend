import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(
                "Необходимо указать адрес электронной почты"
            )
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if not password:
            password = self.make_random_password(length=10)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_superuser=True.'
            )
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        'Уникальный id',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(
        unique=True
    )
    is_client = models.BooleanField(
        'Клиент',
        default=True
    )
    is_psychologists = models.BooleanField(
        'Психолог',
        default=False
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        'Активный',
        default=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_client=True, is_psychologists=False) |
                models.Q(is_psychologists=True, is_client=False),
                name='is_client_or_psychologist'
            )
        ]

    def __str__(self):
        return self.email
