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

    Attributes:
        - rut: Identificador único del cliente en formato RUT.
        - nombre: Nombre del cliente.
        - apellido: Apellido del cliente.
        - correo: Correo electrónico del cliente.
        - telefono: Número de contacto con validación para formato chileno.
        - fecha_registro: Fecha y hora de registro en el sistema.
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
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        """
        Representa al cliente en forma de cadena.

        Returns:
            Una cadena que incluye el nombre completo y el RUT del cliente.
        """
        return f"{self.nombre} {self.apellido} ({self.rut})"


class Trabajador(models.Model):
    """
    Modelo que representa un trabajador del hostal.

    Attributes:
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
    correo = models.EmailField(
        max_length=100,
        validators=[
            EmailValidator(message="Debe ingresar un correo válido.")
        ], blank=True, null=True)  # Nuevo campo correo agregado

    def __str__(self):
        """
        Representa al trabajador en forma de cadena.

        Returns:
            Una cadena que incluye el nombre completo y el RUT del trabajador.
        """
        return f"{self.nombre} {self.apellido} ({self.rut})"


class Habitacion(models.Model):
    """
    Modelo que representa una habitación del hostal.

    Attributes:
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
        """
        Representa la habitación en forma de cadena.

        Returns:
            Una cadena que incluye el número de la habitación y su estado actual.
        """
        return f"Habitación {self.numero_habitacion} - {self.estado}"


class Reserva(models.Model):
    """
    Modelo que representa una reserva.

    Atributos:
        - habitacion: Relación con el modelo Habitacion.
        - trabajador: Relación con el modelo Trabajador.
        - cliente: Relación con el modelo Cliente.
        - origen: Indica cómo se realizó la reserva.
        - estado: Estado actual de la reserva (pendiente, pagada, etc.).
        - fecha_registro: Fecha y hora en que se registró la reserva.
        - noches: Cantidad de noches reservadas.
        - precio_final: Precio total de la reserva.
        - fecha_ingreso: Fecha de inicio de la estadía.
    """
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
        """
        Calcula el valor total de la reserva.

        Basado en:
            - Precio por noche de la habitación.
            - Número de noches reservadas.

        Returns:
            El costo total de la reserva o 0 si no se han definido habitación o noches.
        """
        if self.habitacion and self.noches:
            return self.habitacion.precio * self.noches
        return 0


    def clean(self):
        """
        Realiza una validación personalizada para la reserva.

        Valida que:
            - La habitación no esté ocupada.
            - La fecha de ingreso no sea anterior a la fecha de registro.
            - El precio final sea coherente con el precio calculado.
        """
        if self.fecha_ingreso < self.fecha_registro:
            raise ValidationError("La fecha de ingreso no puede ser anterior a la fecha de registro.")

        if self.habitacion.estado not in ['disponible', 'reservada']:
            raise ValidationError(f"La habitación {self.habitacion.numero_habitacion} no está disponible para reserva.")

        precio_calculado = self.habitacion.precio * self.noches
        if self.precio_final is not None and self.precio_final != precio_calculado:
            raise ValidationError(f"El precio final debe ser {precio_calculado}, pero se ingresó {self.precio_final}.")


    def save(self, *args, **kwargs):
        """
        Realiza validaciones y guarda la reserva.

        Actualiza el estado de la habitación a 'reservada' si la reserva es válida.
        """
        self.clean()
        super().save(*args, **kwargs)
        if self.estado == "pendiente":
            self.habitacion.estado = "reservada"
            self.habitacion.save()

    def __str__(self):
        """
        Representa la reserva en forma de cadena.

        Returns:
            Una cadena que incluye el ID de la reserva y el número de la habitación asociada.
        """
        return f"Reserva {self.id} - Habitación {self.habitacion}"



class CheckIn(models.Model):
    """
    Modelo que representa un registro de entrada (Check-In).

    Attributes:
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
        """
        Representa el registro de entrada (Check-In) en forma de cadena.

        Returns:
            Una cadena que incluye el ID de la reserva asociada al Check-In.
        """
        return f"Check-In de Reserva {self.reserva.id}"


class CheckOut(models.Model):
    """
    Modelo que representa un registro de salida (Check-Out).

    Attributes:
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
        """
        Representa el registro de salida (Check-Out) en forma de cadena.

        Returns:
            Una cadena que incluye el ID de la reserva asociada al Check-Out.
        """
        return f"Check-Out de Reserva {self.reserva.id}"
