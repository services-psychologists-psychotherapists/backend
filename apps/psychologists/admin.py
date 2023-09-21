from django.contrib import admin

from apps.psychologists import models


@admin.register(models.Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_higher')
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.Approach)
class ApproachAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'psychologist', 'type', 'price',
                    'duration', 'format')
    empty_value_display = '-пусто-'
    search_fields = ('title__startswith', )


@admin.register(models.ProfilePsychologist)
class ProfilePsychologistAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'birthday',
                    'gender', 'is_verified', 'speciality')
    empty_value_display = '-пусто-'
    list_filter = ('is_verified', )
    search_fields = ('last_name__startswith', )


@admin.register(models.PsychoEducation)
class PsychoEducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'psychologist', 'institute',
                    'speciality', 'graduation_year')
    empty_value_display = '-пусто-'
