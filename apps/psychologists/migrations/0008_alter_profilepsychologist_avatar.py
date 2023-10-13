# Generated by Django 4.1 on 2023-09-19 15:07

import apps.psychologists.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("psychologists", "0007_alter_profilepsychologist_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profilepsychologist",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=apps.psychologists.models.user_directory_path,
            ),
        ),
    ]
