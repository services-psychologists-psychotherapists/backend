from datetime import date

from django.core.exceptions import ValidationError


def validate_birthday(data):
    today = date.today()
    delta = today.year - data.year - (
        (today.month, today.day) < (data.month, data.day)
    )
    if delta < 18:
        raise ValidationError(
            'Сервис не предоставляет услуги лицам моложе 18 лет.'
        )
    if delta > 150:
        raise ValidationError(
            'Проверьте правильность заполнения даты рождения.'
        )
