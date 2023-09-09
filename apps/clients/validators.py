from datetime import date

from django.core.exceptions import ValidationError

from apps.core.constants import CLIENT_MIN_AGE, MAX_LIFESPAN


def validate_birthday(data):
    today = date.today()
    age = today.year - data.year - (
        (today.month, today.day) < (data.month, data.day)
    )
    if age < CLIENT_MIN_AGE:
        raise ValidationError(
            'Сервис не предоставляет услуги лицам моложе 18 лет.'
        )
    if age > MAX_LIFESPAN:
        raise ValidationError(
            'Проверьте правильность заполнения даты рождения.'
        )
