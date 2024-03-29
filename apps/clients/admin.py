from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "birthday")
    empty_value_display = "-пусто-"
