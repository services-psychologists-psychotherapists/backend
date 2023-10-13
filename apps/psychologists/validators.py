from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.core.constants import MAX_LIFESPAN, PSYCHO_MIN_AGE


def validate_birthday(data):
    now = timezone.now()
    age = now.year - data.year - (
        (now.month, now.day) < (data.month, data.day)
    )
    if age > MAX_LIFESPAN:
        raise ValidationError({"birthday": "Укажите корректный год рождения"})
    if age < PSYCHO_MIN_AGE:
        raise ValidationError(
            {"birthday": "Мы работаем с психологами старше 25 лет"}
        )


def validate_started_working(data):
    now = timezone.now().year
    if data.year > now:
        raise ValidationError(
            {"experience": "Некорректно указан опыт работы"}
        )


def validate_graduation_year(data):
    try:
        finish_year = int(data.split("-")[-1])
    except ValueError:
        raise ValidationError(
            {"graduation_year":
             "Значение поля должно быть вида 'YYYY-YYYY' или 'YYYY'"}
        )
    cur_year = timezone.now().year
    if finish_year > cur_year:
        raise ValidationError(
            {"graduation_year": "Укажите корректный год окончания обучения"}
        )
