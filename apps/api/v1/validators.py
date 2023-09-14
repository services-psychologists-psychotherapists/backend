from rest_framework.serializers import ValidationError

from apps.core.constants import FILE_MAX_SIZE


def validate_file_size(file_obj):
    if file_obj.size > FILE_MAX_SIZE:
        raise ValidationError(
            'Максимальный размер файла 2 Мб'
        )
