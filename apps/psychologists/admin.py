from django.contrib import admin

from apps.psychologists import models


@admin.register(models.Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ('title', )
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.Approach)
class ApproachAdmin(admin.ModelAdmin):
    list_display = ('title', )
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.ProfilePsychologist)
class ProfilePsychologistAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthdate',
                    'gender', 'is_verified')
    empty_value_display = '-пусто-'
    list_filter = ('is_verified', )
    search_fields = ('last_name__startswith', )


@admin.register(models.PsychoEducation)
class PsychoEducationAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
