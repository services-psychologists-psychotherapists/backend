from django.shortcuts import get_object_or_404

from apps.core.models import UploadFile


def get_file(file_id):
    return get_object_or_404(UploadFile, id=file_id)
