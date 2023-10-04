from time import time

from .models import UploadFile


def create_file(validated_data):
    name = int(time())
    ext = validated_data['path'].name.split('.')[-1]
    validated_data['path'].name = f'{name}.{ext}'
    file = UploadFile.objects.create(
        **validated_data
    )
    return file
