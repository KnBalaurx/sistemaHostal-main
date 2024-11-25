"""
Configuración de URLs para el proyecto sistemaHostal.

Este archivo define las rutas principales del proyecto y las asocia
a las vistas correspondientes en la aplicación `gestion`. Cada entrada
de `urlpatterns` incluye:
- Una URL específica.
- Una vista asociada que maneja la lógica para esa URL.
- Un nombre único para la ruta (opcional) que permite referenciarla en otras partes del proyecto.

"""

from django.contrib import admin
from django.urls import path
from gestion import views  

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # Panel de administración de Django.
    path('login', views.login_trabajador, name='login'),  # Ruta para el inicio de sesión de trabajadores.
    path('logout/', views.logout_trabajador, name='logout'),  # Ruta para cerrar sesión de trabajadores.
    path('', views.home, name='home'),  # Página de inicio del sistema.
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),  # Formulario para agregar un nuevo cliente.
    path('agregar-reserva/', views.agregar_reserva, name='agregar_reserva'),  # Formulario para crear una nueva reserva.
    path('tabla-clientes/', views.tabla_clientes, name='tabla_clientes'),  # Tabla con la lista de clientes.
    path('reserva/editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),  # Editar una reserva específica usando su `pk`.
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),  # Editar un cliente específico por su `cliente_id`.
    path('tabla-habitaciones/', views.tabla_habitaciones, name='tabla_habitaciones'),  # Tabla con la lista de habitaciones disponibles.
]
