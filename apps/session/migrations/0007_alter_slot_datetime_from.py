# Generated by Django 4.1 on 2023-10-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0006_merge_20230928_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='datetime_from',
            field=models.DateTimeField(db_index=True, verbose_name='Начало сессии'),
        ),
    ]