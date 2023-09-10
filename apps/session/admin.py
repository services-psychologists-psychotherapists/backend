from django.contrib import admin

from .models import Session, Slot


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Настройка сессии для админки"""
    list_display = (
        'client',
        'slot',
        'status'
    )


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    """Настройка окна записи для админки"""
    list_display = (
        'psychologist',
        'datetime_from',
        'datetime_to',
        'is_free'
    )
