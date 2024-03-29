# Generated by Django 4.1 on 2023-09-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='customuser',
            name='is_client_or_psychologist',
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('is_client', True), ('is_psychologists', False)), models.Q(('is_client', False), ('is_psychologists', True)), _connector='OR'), name='is_client_or_psychologist'),
        ),
    ]
