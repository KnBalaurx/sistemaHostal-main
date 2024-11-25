# Generated by Django 3.2 on 2024-11-24 15:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('password_hash', models.CharField(max_length=255)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_habitacion', models.CharField(max_length=10, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('reservada', 'Reservada'), ('mantenimiento', 'En Mantenimiento')], default='disponible', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_habitacion', models.CharField(max_length=10)),
                ('origen', models.CharField(choices=[('manual', 'Manual'), ('otra_plataforma', 'Otra Plataforma')], default='manual', max_length=20)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada'), ('finalizada', 'Finalizada')], default='pendiente', max_length=15)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion.cliente')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.habitacion')),
                ('trabajador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion.trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('qr_escaneado', models.CharField(choices=[('sí', 'Sí'), ('no', 'No')], default='no', max_length=2)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('qr_escaneado', models.CharField(choices=[('sí', 'Sí'), ('no', 'No')], default='no', max_length=2)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.reserva')),
            ],
        ),
    ]