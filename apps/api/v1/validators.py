from rest_framework.serializers import ValidationError

from apps.core.constants import FILE_MAX_SIZE, ALLOWED_FORMAT


def validate_file_size(file_obj):
    if file_obj.size > FILE_MAX_SIZE:
        raise ValidationError(
            'Максимальный размер файла 2 Мб'
        )


def validate_file_ext(file_obj):
    ext = file_obj.name.split('.')[-1].lower()
    if ext not in ALLOWED_FORMAT:
        raise ValidationError(
            f"Допустимые разрешения файлов: {ALLOWED_FORMAT}"
        )
