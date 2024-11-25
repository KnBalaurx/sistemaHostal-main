from django.contrib import admin
from gestion.models import Cliente, Trabajador, Habitacion, Reserva, CheckIn, CheckOut

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Cliente.

    - `list_display`: Campos que se mostrarán en la vista de lista del panel de administración.
    - `search_fields`: Campos que estarán disponibles para la búsqueda en el panel de administración.
    - `list_filter`: Campos por los que se podrá filtrar en la vista de lista del panel de administración.
    """
    list_display = ('rut', 'nombre', 'apellido', 'correo', 'telefono', 'fecha_registro')
    search_fields = ('rut', 'nombre', 'apellido', 'correo')
    list_filter = ('fecha_registro',)

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Trabajador.

    - `list_display`: Campos que se mostrarán en la vista de lista del panel de administración.
    - `search_fields`: Campos que estarán disponibles para la búsqueda en el panel de administración.
    """
    list_display = ('rut', 'nombre', 'apellido')
    search_fields = ('rut', 'nombre', 'apellido')

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Habitación.

    - `list_display`: Campos que se mostrarán en la vista de lista del panel de administración.
    - `search_fields`: Campos que estarán disponibles para la búsqueda en el panel de administración.
    - `list_filter`: Campos por los que se podrá filtrar en la vista de lista del panel de administración.
    """
    list_display = ('numero_habitacion', 'precio', 'estado')
    search_fields = ('numero_habitacion',)
    list_filter = ('estado',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Reserva.

    - `list_display`: Campos que se mostrarán en la vista de lista del panel de administración.
    - `list_filter`: Campos por los que se podrá filtrar en la vista de lista del panel de administración.
    - `search_fields`: Campos que estarán disponibles para la búsqueda en el panel de administración.
    """
    list_display = (
        'id', 'cliente', 'habitacion', 'estado', 
        'fecha_registro', 'fecha_ingreso', 'noches', 'valor_total'
    )
    list_filter = ('estado', 'fecha_registro', 'habitacion')
    search_fields = ('cliente__nombre', 'habitacion__numero_habitacion')

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo CheckIn.

    - `list_display`: Campos que se mostrarán en la vista de lista del panel de administración.
    - `search_fields`: Campos que estarán disponibles para la búsqueda en el panel de administración.
    - `list_filter`: Campos por los que se podrá filtrar en la vista de lista del panel de administración.
    """
    list_display = ('id', 'reserva', 'fecha_hora', 'qr_escaneado')
    search_fields = ('reserva__id', 'reserva__cliente__rut')
    list_filter = ('fecha_hora', 'qr_escaneado')

@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo CheckOut.

    - `list_display`: Campos que se mostrarán en la vista de lista del panel de administración.
    - `search_fields`: Campos que estarán disponibles para la búsqueda en el panel de administración.
    - `list_filter`: Campos por los que se podrá filtrar en la vista de lista del panel de administración.
    """
    list_display = ('id', 'reserva', 'fecha_hora', 'qr_escaneado')
    search_fields = ('reserva__id', 'reserva__cliente__rut')
    list_filter = ('fecha_hora', 'qr_escaneado')



