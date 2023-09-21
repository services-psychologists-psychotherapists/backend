from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'is_client', 'is_psychologists', 'is_active'
    )
    empty_value_display = '-пусто-'
