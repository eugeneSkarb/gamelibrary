# Generated by Django 3.1.5 on 2021-01-11 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_game_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamestudio',
            name='founder',
        ),
    ]
