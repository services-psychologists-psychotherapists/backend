# Generated by Django 4.1 on 2023-09-20 16:18

import apps.psychologists.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psychologists', '0008_alter_profilepsychologist_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepsychologist',
            name='birthday',
            field=models.DateField(validators=[apps.psychologists.validators.validate_birthday]),
        ),
        migrations.AlterField(
            model_name='profilepsychologist',
            name='started_working',
            field=models.DateField(validators=[apps.psychologists.validators.validate_started_working]),
        ),
        migrations.AlterField(
            model_name='psychoeducation',
            name='graduation_year',
            field=models.CharField(max_length=10, validators=[apps.psychologists.validators.validate_graduation_year]),
        ),
    ]