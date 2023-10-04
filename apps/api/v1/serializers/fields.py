import base64
from time import time

from django.core.files.base import ContentFile
from rest_framework import serializers

from apps.core.selectors import get_file


class ImageFieldSerialiser(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f'{int(time())}.{ext}'
            data = ContentFile(base64.b64decode(imgstr), name=file_name)
        return super().to_internal_value(data)


class FilePathSerializer(serializers.FileField):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        file = get_file(value)
        return super().to_representation(file.path)
