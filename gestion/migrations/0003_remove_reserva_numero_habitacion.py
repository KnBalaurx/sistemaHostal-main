# Generated by Django 3.2 on 2024-11-25 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_auto_20241125_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='numero_habitacion',
        ),
    ]