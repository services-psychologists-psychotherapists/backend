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


class PsychoEducationInline(admin.TabularInline):
    model = models.PsychoEducation
    extra = 1


class ServiceInline(admin.TabularInline):
    model = models.Service
    extra = 1


@admin.register(models.ProfilePsychologist)
class ProfilePsychologistAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ("user", "is_verified")}),
        (
            "Общая информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birthday",
                    "gender",
                    "phone_number",
                    "about",
                    "started_working",
                )
            },
        ),
        ("О работе", {"fields": ["themes", "approaches"]}),
    ]
    inlines = (PsychoEducationInline, ServiceInline)
    list_display = (
        "user",
        "first_name",
        "last_name",
        "birthday",
        "gender",
        "is_verified",
        "speciality",
    )
    empty_value_display = "-пусто-"
    list_filter = ("is_verified",)
    search_fields = ("last_name__startswith",)
    actions = ("send_activation_email",)

    def save_model(self, request, obj, form, change):
        if 'is_verified' in form.changed_data:
            obj.save(update_fields=['is_verified'])
        else:
            obj.save()
