from django.contrib import admin

from apps.core import models


@admin.register(models.Gender)
class GenderAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
