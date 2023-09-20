import base64
from time import time

from django.core.files.base import ContentFile
from rest_framework import serializers


class ImageFieldSerialiser(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f'{int(time())}.{ext}'
            data = ContentFile(base64.b64decode(imgstr), name=file_name)
        return super().to_internal_value(data)
