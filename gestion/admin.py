from django.contrib import admin
from .models import Cliente, Trabajador, Habitacion, Reserva, CheckIn, CheckOut




@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'correo', 'telefono', 'fecha_registro')
    search_fields = ('rut', 'nombre', 'apellido', 'correo')
    list_filter = ('fecha_registro',)



@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido')
    search_fields = ('rut', 'nombre', 'apellido')



@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero_habitacion', 'precio', 'estado')
    search_fields = ('numero_habitacion',)
    list_filter = ('estado',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'habitacion', 'estado', 'fecha_registro', 'fecha_ingreso', 'noches', 'valor_total')
    list_filter = ('estado', 'fecha_registro', 'habitacion')
    search_fields = ('cliente__nombre', 'habitacion__numero_habitacion')


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'fecha_hora', 'qr_escaneado')
    search_fields = ('reserva__id', 'reserva__cliente__rut')
    list_filter = ('fecha_hora', 'qr_escaneado')



@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'fecha_hora', 'qr_escaneado')
    search_fields = ('reserva__id', 'reserva__cliente__rut')
    list_filter = ('fecha_hora', 'qr_escaneado')


