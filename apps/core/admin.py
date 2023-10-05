from django.contrib import admin

from .models import UploadFile


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'path')
    empty_value_display = '-пусто-'
