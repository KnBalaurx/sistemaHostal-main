"""
Configuración de URLs para el proyecto sistemaHostal.

Este archivo define las rutas principales del proyecto y las asocia
a las vistas correspondientes en la aplicación `gestion`.

Para más información, consulta la documentación oficial de Django:
https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # URL para el panel de administración.
    path('login', views.login_trabajador, name='login'),  # URL para el inicio de sesión.
    path('logout/', views.logout_trabajador, name='logout'),  # URL para cerrar sesión.
    path('', views.home, name='home'),  # Página principal del sistema.
    path('agregar-cliente/', views.agregar_cliente, name='agregar_cliente'),  # URL para agregar clientes.
    path('agregar-reserva/', views.agregar_reserva, name='agregar_reserva'),  # URL para agregar reservas.
    path('tabla-clientes/', views.tabla_clientes, name='tabla_clientes'),  # URL para visualizar clientes.
    path("reserva/editar/<int:pk>/", views.editar_reserva, name="editar_reserva"),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('reserva/editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
    path('tabla-habitaciones/', views.tabla_habitaciones, name='tabla_habitaciones'),  # URL para visualizar habitaciones.
]
