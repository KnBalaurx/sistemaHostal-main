from django.test import TestCase
from django.utils import timezone
from .models import Cliente, Trabajador, Habitacion, Reserva
from django.core.exceptions import ValidationError


class ClienteModelTest(TestCase):

    def test_create_cliente(self):
        cliente = Cliente.objects.create(
            rut='12345678-9',
            nombre='Juan',
            apellido='Pérez',
            correo='juan.perez@example.com',
            telefono='+56912345678',
            fecha_registro=timezone.now()
        )
        self.assertEqual(cliente.nombre, 'Juan')


class TrabajadorModelTest(TestCase):

    def test_create_trabajador(self):
        trabajador = Trabajador.objects.create(
            rut='87654321-1',
            nombre='Carlos',
            apellido='González'
        )
        self.assertEqual(trabajador.nombre, 'Carlos')


class HabitacionModelTest(TestCase):

    def test_create_habitacion(self):
        habitacion = Habitacion.objects.create(
            numero_habitacion='101',
            precio=50000.00,
            estado='disponible'
        )
        self.assertEqual(habitacion.estado, 'disponible')


class ReservaModelTest(TestCase):

    def test_create_reserva(self):
        habitacion = Habitacion.objects.create(
            numero_habitacion='102',
            precio=60000.00,
            estado='disponible'
        )
        cliente = Cliente.objects.create(
            rut='11223344-5',
            nombre='Ana',
            apellido='Rodríguez',
            correo='ana.rodriguez@example.com',
            telefono='+56911223344',
            fecha_registro=timezone.now()
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
            precio_final=120000.00,
            fecha_ingreso=timezone.now()
        )
        self.assertEqual(reserva.precio_final, 120000.00)

    def test_habitacion_ocupada_no_disponible(self):
        habitacion = Habitacion.objects.create(
            numero_habitacion='104',
            precio=75000.00,
            estado='disponible'
        )
        cliente = Cliente.objects.create(
            rut='77665544-3',
            nombre='Javier',
            apellido='Muñoz',
            correo='javier.munoz@example.com',
            telefono='+56977665544',
            fecha_registro=timezone.now()
        )
        trabajador = Trabajador.objects.create(
            rut='33445566-7',
            nombre='Sofía',
            apellido='Pérez'
        )

        # Crear una reserva inicial
        Reserva.objects.create(
            habitacion=habitacion,
            trabajador=trabajador,
            cliente=cliente,
            origen='manual',
            estado='confirmada',
            noches=3,
            precio_final=225000.00,
            fecha_ingreso=timezone.now()
        )
        habitacion.estado = 'ocupada'
        habitacion.save()

        nueva_reserva = Reserva(
            habitacion=habitacion,
            trabajador=trabajador,
            cliente=cliente,
            origen='manual',
            estado='pendiente',
            noches=2,
            precio_final=150000.00,
            fecha_ingreso=timezone.now()
        )

        with self.assertRaises(ValidationError):
            nueva_reserva.full_clean()  # Llama explícitamente a las validaciones del modelo

    def test_precio_final_invalido(self):
        habitacion = Habitacion.objects.create(
            numero_habitacion='105',
            precio=80000.00,
            estado='disponible'
        )
        cliente = Cliente.objects.create(
            rut='44556677-8',
            nombre='Clara',
            apellido='Ortiz',
            correo='clara.ortiz@example.com',
            telefono='+56944556677',
            fecha_registro=timezone.now()
        )
        trabajador = Trabajador.objects.create(
            rut='55667788-9',
            nombre='Hugo',
            apellido='Lopez'
        )

        reserva = Reserva(
            habitacion=habitacion,
            trabajador=trabajador,
            cliente=cliente,
            origen='manual',
            estado='pendiente',
            noches=3,
            precio_final=100000.00,  # Precio no corresponde al calculado
            fecha_ingreso=timezone.now()
        )

        with self.assertRaises(ValidationError):
            reserva.full_clean()
