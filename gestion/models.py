"""
Definición de los modelos de la aplicación gestion.

Estos modelos representan las entidades principales del sistema,
como clientes, trabajadores, habitaciones, reservas y registros de
check-in/check-out.
"""
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, EmailValidator
from django.forms import ValidationError
from django.utils.timezone import now


class Cliente(models.Model):
    """
    Modelo que representa un cliente del hostal con validaciones completas.
    """
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[0-9kK]$',
                message="El RUT debe estar en el formato 12345678-9."
            )])
    nombre = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message="El nombre solo puede contener letras y espacios."
            )])
    apellido = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message="El apellido solo puede contener letras y espacios."
            )])
    correo = models.EmailField(
        max_length=100,
        validators=[
            EmailValidator(message="Debe ingresar un correo válido.")
        ])
    telefono = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\+569\d{8}$',
                message="El número de teléfono debe estar en el formato '+56912345678'."
            )], help_text="Debe ingresar un número con el formato '+56912345678'.")
    password_hash = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"



class Trabajador(models.Model):
    """
    Modelo que representa un trabajador del hostal.

    Atributos:
        - rut: Identificador único del trabajador.
        - nombre: Nombre del trabajador.
        - apellido: Apellido del trabajador.
    """
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7,8}-[0-9kK]$',
                message="El RUT debe estar en el formato 1234567-9."
            )])
    nombre = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message="El nombre solo puede contener letras y espacios."
            )])
    apellido = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message="El apellido solo puede contener letras y espacios."
            )])

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"


class Habitacion(models.Model):
    """
    Modelo que representa una habitación del hostal.

    Atributos:
        - numero_habitacion: Número identificador de la habitación.
        - precio: Precio de la habitación.
        - estado: Estado actual de la habitación (disponible, reservada, etc.).
    """
    numero_habitacion = models.CharField(max_length=10, unique=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0, message="El precio debe ser un valor positivo.")])
    estado = models.CharField(max_length=15, choices=[
        ("disponible", "Disponible"),
        ("reservada", "Reservada"),
        ("mantenimiento", "En Mantenimiento"),
        ("en uso", "En Uso"),
    ], default="disponible")

    def __str__(self):
        return f"Habitación {self.numero_habitacion} - {self.estado}"


class Reserva(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    origen = models.CharField(max_length=20, choices=[
        ("manual", "Manual"),
        ("otra_plataforma", "Otra Plataforma")
    ], default="manual")
    estado = models.CharField(max_length=15, choices=[
        ("pendiente", "Pendiente"),
        ("pagada", "Pagada"),
        ("cancelada", "Cancelada")
    ], default="pendiente")
    fecha_registro = models.DateTimeField(default=now)
    noches = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message="Debe haber al menos una noche en la reserva.")
        ])
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_ingreso = models.DateTimeField(default=now, blank=True)
    
    @property
    def valor_total(self):
        if self.habitacion and self.noches:
            return self.habitacion.precio * self.noches
        return 0
    
    def clean(self):
        """Método para validar que la fecha de ingreso no sea anterior a la fecha de registro"""
        if self.fecha_ingreso < self.fecha_registro:
            raise ValidationError('La fecha de ingreso no puede ser anterior a la fecha de registro.')

    def __str__(self):
        return f"Reserva {self.id} - Habitación {self.habitacion}"


class CheckIn(models.Model):
    """
    Modelo que representa un registro de entrada (Check-In).

    Atributos:
        - reserva: Reserva asociada al Check-In.
        - fecha_hora: Fecha y hora del Check-In.
        - qr_escaneado: Indica si el QR fue escaneado.
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=now)
    qr_escaneado = models.CharField(max_length=2, choices=[
        ("sí", "Sí"),
        ("no", "No"),
    ], default="no")

    def __str__(self):
        return f"Check-In de Reserva {self.reserva.id}"


class CheckOut(models.Model):
    """
    Modelo que representa un registro de salida (Check-Out).

    Atributos:
        - reserva: Reserva asociada al Check-Out.
        - fecha_hora: Fecha y hora del Check-Out.
        - qr_escaneado: Indica si el QR fue escaneado.
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=now)
    qr_escaneado = models.CharField(max_length=2, choices=[
        ("sí", "Sí"),
        ("no", "No"),
    ], default="no")

    def __str__(self):
        return f"Check-Out de Reserva {self.reserva.id}"
