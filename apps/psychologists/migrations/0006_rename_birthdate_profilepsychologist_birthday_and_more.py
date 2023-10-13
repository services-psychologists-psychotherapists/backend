# Generated by Django 4.1 on 2023-09-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("psychologists", "0005_remove_psychoeducation_unique_education_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profilepsychologist",
            old_name="birthdate",
            new_name="birthday",
        ),
        migrations.AddField(
            model_name="profilepsychologist",
            name="speciality",
            field=models.CharField(blank=True, default="Психолог", max_length=50),
        ),
    ]
