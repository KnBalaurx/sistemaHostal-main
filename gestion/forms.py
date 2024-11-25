"""
Definición de formularios utilizados en la aplicación gestion.

Estos formularios están basados en los modelos Cliente y Reserva.
Se utilizan para validar y procesar datos ingresados por el usuario
en las interfaces de la aplicación.
"""
from django import forms
from gestion.models import Cliente, Reserva

class ClienteForm(forms.ModelForm):
    """
    Formulario para manejar la creación y edición de clientes.

    Campos:
        - rut: Identificador único del cliente.
        - nombre: Nombre del cliente.
        - apellido: Apellido del cliente.
        - correo: Correo electrónico del cliente.
        - telefono: Teléfono de contacto del cliente.
    """
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'correo', 'telefono']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReservaForm(forms.ModelForm):
    """
    Formulario para manejar la creación y edición de reservas.
    """
    class Meta:
        model = Reserva
        fields = [
            'habitacion',
            'cliente',
            'origen',
            'estado',
            'fecha_ingreso', 
            'noches',
        ]
        widgets = {
            'habitacion': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'origen': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Cambia aquí
            'noches': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
