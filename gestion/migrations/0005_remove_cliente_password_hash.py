# Generated by Django 3.2 on 2024-11-25 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_auto_20241125_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='password_hash',
        ),
    ]
