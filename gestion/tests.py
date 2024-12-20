from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Cliente, Trabajador, Habitacion, Reserva
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta

class ReservaIntegradaTest(TestCase):

    # 1. Prueba Integral de Creación de Reserva
    def test_crear_reserva(self):
        # Crear un cliente
        cliente = Cliente.objects.create(
            rut='12345678-9',
            nombre='Carlos',
            apellido='Pérez',
            correo='carlos.perez@example.com',
            telefono='+56987654321',
            fecha_registro=timezone.now()
        )

        # Crear una habitación
        habitacion = Habitacion.objects.create(
            numero_habitacion='101',
            precio=50000.00,
            estado='disponible'
        )

        # Crear un trabajador
        trabajador = Trabajador.objects.create(
            rut='22334455-6',
            nombre='Luis',
            apellido='Martínez'
        )

        # Crear la reserva
        reserva = Reserva.objects.create(
            habitacion=habitacion,
            trabajador=trabajador,
            cliente=cliente,
            origen='manual',
            estado='pendiente',
            noches=2,
            precio_final=100000.00,
            fecha_ingreso=timezone.now() + timezone.timedelta(days=1)
        )

        # Verificar que el estado de la habitación cambió a "reservada"
        habitacion.refresh_from_db()
        self.assertEqual(habitacion.estado, 'reservada')

        # Verificar que la reserva se guardó correctamente
        self.assertEqual(reserva.estado, 'pendiente')
        self.assertEqual(reserva.precio_final, 100000.00)

    # 2. Prueba Integral de Reserva con Fecha de Ingreso Pasada
    def test_crear_reserva_fecha_ingreso_pasada(self):
        # Crear una habitación
        habitacion = Habitacion.objects.create(
            numero_habitacion="101",  # Usar el nombre correcto del campo
            estado="disponible",
            precio=100.00,
        )

        # Crear una reserva con fecha de ingreso pasada
        reserva = Reserva(
            habitacion=habitacion,
            fecha_ingreso=now() - timedelta(days=1),  # Fecha en el pasado
            noches=2,
            estado="pendiente",
        )

        # Asegurarse de que se lanza ValidationError al intentar validar
        with self.assertRaises(ValidationError):
            reserva.full_clean()  # Ejecuta las validaciones definidas en clean()

    # 3. Prueba Integral de Cancelación de Reserva
    def test_cancelar_reserva(self):
        cliente = Cliente.objects.create(
            rut='12345678-9',
            nombre='Carlos',
            apellido='Pérez',
            correo='carlos.perez@example.com',
            telefono='+56987654321',
            fecha_registro=timezone.now()
        )

        habitacion = Habitacion.objects.create(
            numero_habitacion='103',
            precio=50000.00,
            estado='reservada'
        )

        trabajador = Trabajador.objects.create(
            rut='22334455-6',
            nombre='Luis',
            apellido='Martínez'
        )

        reserva = Reserva.objects.create(
            habitacion=habitacion,
            trabajador=trabajador,
            cliente=cliente,
            origen='manual',
            estado='pendiente',
            noches=2,
            precio_final=100000.00,
            fecha_ingreso=timezone.now() + timezone.timedelta(days=1)
        )

        # Cancelar la reserva
        reserva.estado = 'cancelada'
        reserva.save()

        # Verificar que la habitación vuelva a estar disponible
        habitacion.refresh_from_db()
        self.assertEqual(habitacion.estado, 'disponible')

    # 4. Prueba Integral de Creación de Cliente con Correo Único
    def test_crear_cliente_con_correo_unico(self):
        Cliente.objects.create(nombre="Carlos Perez", correo="carlos.perezz@example.com")
        with self.assertRaises(IntegrityError):
            Cliente.objects.create(nombre="Carlos Pérez II", correo="carlos.perezz@example.com")

    # 5. Prueba Integral de Actualización de Precio de Reserva
    def test_actualizar_precio_reserva(self):
        cliente = Cliente.objects.create(
            rut='12345678-9',
            nombre='Carlos',
            apellido='Pérez',
            correo='carlos.perez@example.com',
            telefono='+56987654321',
            fecha_registro=timezone.now()
        )

        habitacion = Habitacion.objects.create(
            numero_habitacion='104',
            precio=50000.00,
            estado='disponible'
        )

        trabajador = Trabajador.objects.create(
            rut='22334455-6',
            nombre='Luis',
            apellido='Martínez'
        )

        reserva = Reserva.objects.create(
            habitacion=habitacion,
            trabajador=trabajador,
            cliente=cliente,
            origen='manual',
            estado='pendiente',
            noches=3,
            precio_final=150000.00,
            fecha_ingreso=timezone.now() + timezone.timedelta(days=1)
        )

        # Actualizar el precio de la reserva
        reserva.precio_final = 180000.00
        reserva.save()

        # Verificar que el precio se actualizó correctamente
        reserva.refresh_from_db()
        self.assertEqual(reserva.precio_final, 180000.00)

    # 6. Prueba Integral de Crear Trabajador y Asignar a Reserva
    def test_asignar_trabajador_a_reserva(self):
        cliente = Cliente.objects.create(
            rut='12345678-9',
            nombre='Carlos',
            apellido='Pérez',
            correo='carlos.perez@example.com',
            telefono='+56987654321',
            fecha_registro=timezone.now()
        )

        habitacion = Habitacion.objects.create(
            numero_habitacion='105',
            precio=50000.00,
            estado='disponible'
        )

        trabajador = Trabajador.objects.create(
            rut='22334455-6',
            nombre='Luis',
            apellido='Martínez'
        )

        reserva = Reserva.objects.create(
            habitacion=habitacion,
            trabajador=trabajador,
            cliente=cliente,
            origen='manual',
            estado='pendiente',
            noches=2,
            precio_final=100000.00,
            fecha_ingreso=timezone.now() + timezone.timedelta(days=1)
        )

        # Verificar que el trabajador está asociado correctamente a la reserva
        self.assertEqual(reserva.trabajador.nombre, 'Luis')
        self.assertEqual(reserva.trabajador.rut, '22334455-6')
