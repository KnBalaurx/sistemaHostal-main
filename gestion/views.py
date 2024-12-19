from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse  
from gestion.models import Trabajador, Reserva, Cliente, Habitacion
from gestion.forms import ClienteForm, ReservaForm
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

def login_trabajador(request):
    """
    Maneja el inicio de sesión para los trabajadores del sistema.

    Este método permite autenticar a un trabajador utilizando su RUT y una contraseña generada a partir de sus datos personales.
    Si las credenciales son correctas, se almacena la sesión del trabajador y se redirige a la página principal.

    Attributes:
        request: Solicitud HTTP que contiene los datos del formulario de inicio de sesión.

    Returns:
        HttpResponse: Página de inicio de sesión o redirección a la página principal si el login es exitoso.
    """
    if request.method == "POST":
        rut = request.POST.get("rut")
        password = request.POST.get("password")

        if not rut or not password:
            messages.error(request, "Por favor, ingrese su RUT y contraseña.")
            return render(request, 'gestion/login.html')

        try:
            trabajador = Trabajador.objects.get(rut=rut)
            expected_password = trabajador.apellido[:3].lower() + trabajador.nombre[:3].lower()

            if password.lower() == expected_password:
                request.session['trabajador_id'] = trabajador.id
                request.session['trabajador_nombre'] = f"{trabajador.nombre} {trabajador.apellido}"
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect('home')
            else:
                messages.error(request, "Credenciales incorrectas.")
        except Trabajador.DoesNotExist:
            messages.error(request, "Credenciales incorrectas.")
    
    return render(request, 'gestion/login.html')

def logout_trabajador(request):
    """
    Finaliza la sesión activa de un trabajador y lo redirige al formulario de inicio de sesión.

    Attributes:
        request: Solicitud HTTP.

    Returns:
        HttpResponse: Redirección a la página de inicio de sesión.
    """
    logout(request)
    return redirect('login')


def agregar_cliente(request):
    """
    Procesa un formulario para registrar un nuevo cliente en el sistema.

    Permite al trabajador completar un formulario con los datos del cliente. Si el formulario es válido, 
    el cliente se guarda en la base de datos.

    Attributes:
        request: Solicitud HTTP que puede contener datos de un formulario enviado por POST.

    Returns:
        HttpResponse: Página con el formulario vacío o con errores, o redirección si se guarda exitosamente.
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla_clientes')
        else:
            return render(request, 'gestion/agregar_cliente.html', {'form': form})
    else:
        form = ClienteForm()
        return render(request, 'gestion/agregar_cliente.html', {'form': form})

def editar_cliente(request, cliente_id):
    """
    Permite modificar los datos de un cliente existente.

    Carga los datos de un cliente específico y los prellena en un formulario para que puedan ser actualizados.

    Attributes:
        request: Solicitud HTTP que puede contener datos de un formulario enviado por POST.
        cliente_id: ID del cliente a editar.

    Returns:
        HttpResponse: Página con el formulario prellenado o con errores, o redirección tras guardar.
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect(reverse('tabla_clientes'))
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'gestion/editar_cliente.html', {'form': form, 'cliente': cliente})

def agregar_reserva(request):
    """
    Maneja la creación de nuevas reservas para habitaciones.

    Incluye lógica para calcular el costo total basado en el precio de la habitación y el número de noches, 
    además de actualizar el estado de la habitación.

    Attributes:
        request: Solicitud HTTP que puede contener datos de un formulario enviado por POST.

    Returns:
        HttpResponse: Página con el formulario vacío o con errores, o redirección si la reserva se guarda exitosamente.
    """
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            habitacion = form.cleaned_data['habitacion']
            fecha_ingreso = form.cleaned_data['fecha_ingreso']
            noches = form.cleaned_data['noches']
            fecha_registro = datetime.now()

            # Validar que la fecha de ingreso no sea anterior a la actual
            if fecha_ingreso < now():
                messages.error(request, "La fecha de ingreso no puede ser anterior a la actual.")
                return render(request, 'gestion/agregar_reserva.html', {'form': form})

            # Verificar si la habitación está ocupada
            if habitacion.estado == "ocupada":
                messages.error(request, "La habitación está ocupada y no puede ser reservada.")
                return render(request, 'gestion/agregar_reserva.html', {'form': form})

            precio_final = habitacion.precio * noches
            reserva = form.save(commit=False)
            reserva.precio_final = precio_final
            reserva.estado = "pendiente"
            reserva.fecha_registro = fecha_registro
            reserva.save()

            habitacion.estado = "reservada"
            habitacion.save()

            messages.success(request, "Reserva agregada correctamente.")
            return redirect('home')  # Redirige a la página principal después de crear la reserva
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ReservaForm()

    habitaciones_disponibles = Habitacion.objects.filter(estado="disponible")
    data = {'form': form, 'habitaciones': habitaciones_disponibles}
    return render(request, 'gestion/agregar_reserva.html', data)
def editar_reserva(request, pk):
    """
    Permite editar una reserva existente.

    Carga los datos de una reserva específica para que puedan ser actualizados mediante un formulario.

    Attributes:
        request: Solicitud HTTP que puede contener datos de un formulario enviado por POST.
        pk: ID de la reserva a editar.

    Returns:
        HttpResponse: Página con el formulario prellenado o con errores, o redirección tras guardar.
    """
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva actualizada correctamente.")
            return redirect("home")
        else:
            messages.error(request, "Corrige el formulario.")
    else:
        form = ReservaForm(instance=reserva)
    return render(request, "gestion/editar_reserva.html", {"form": form, "reserva": reserva})

def home(request):
    """
    Renderiza la página principal del sistema.

    Muestra las reservas activas y permite acceder a otras funciones del sistema,
    siempre que el trabajador haya iniciado sesión correctamente.

    Attributes:
        request: Solicitud HTTP.

    Returns:
        HttpResponse: Página principal del sistema o redirección al login si no hay sesión activa.
    """
    trabajador_id = request.session.get('trabajador_id')
    if not trabajador_id:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    try:
        trabajador = Trabajador.objects.get(id=trabajador_id)
    except Trabajador.DoesNotExist:
        del request.session['trabajador_id']
        messages.error(request, "Tu sesión no es válida. Por favor, inicia sesión nuevamente.")
        return redirect('login')

    reservas = Reserva.objects.all()
    cliente_form = ClienteForm()
    reserva_form = ReservaForm()
    data = {
        'trabajador': trabajador,
        'reservas': reservas,
        'cliente_form': cliente_form,
        'reserva_form': reserva_form,
    }
    return render(request, 'gestion/home.html', data)

def tabla_clientes(request):
    """
    Muestra una lista con todos los clientes registrados.

    Solo permite el acceso si hay un trabajador autenticado en la sesión.

    Attributes:
        request: Solicitud HTTP.

    Returns:
        HttpResponse: Página con la tabla de clientes o redirección al login si no hay sesión activa.
    """
    if 'trabajador_id' not in request.session:
        return redirect('login')

    clientes = Cliente.objects.all()
    trabajador = request.session['trabajador_nombre']
    data = {'clientes': clientes, 'trabajador': trabajador}
    return render(request, 'gestion/clientes.html', data)

def tabla_habitaciones(request):
    """
    Muestra una lista con todas las habitaciones disponibles en el sistema.

    Solo permite el acceso si hay un trabajador autenticado en la sesión.

    Attributes:
        request: Solicitud HTTP.

    Returns:
        HttpResponse: Página con la tabla de habitaciones o redirección al login si no hay sesión activa.
    """
    if 'trabajador_id' not in request.session:
        return redirect('login')

    habitaciones = Habitacion.objects.all()
    trabajador = request.session['trabajador_nombre']
    data = {'habitaciones': habitaciones, 'trabajador': trabajador}
    return render(request, 'gestion/habitaciones.html', data)
