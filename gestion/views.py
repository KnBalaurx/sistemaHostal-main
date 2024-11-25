from datetime import datetime, timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse # type: ignore
from gestion.models import Trabajador, Reserva, Cliente, Habitacion
from gestion.forms import ClienteForm, ReservaForm
from django.shortcuts import get_object_or_404

def login_trabajador(request):
    """
    Procesa el inicio de sesión para trabajadores.
    Si el método es POST, autentica al trabajador usando RUT y contraseña.
    """
    if request.method == "POST":
        # Recupera los datos enviados desde el formulario
        rut = request.POST.get("rut")
        password = request.POST.get("password")

        # Validar que se proporcionen ambos campos
        if not rut or not password:
            messages.error(request, "Por favor, ingrese su RUT y contraseña.")
            return render(request, 'gestion/login.html')

        try:
            # Busca al trabajador en la base de datos por su RUT
            trabajador = Trabajador.objects.get(rut=rut)

            # Genera la contraseña esperada basada en el apellido y nombre
            # Nota: Esta lógica debería mejorarse en un entorno real
            expected_password = trabajador.apellido[:3].lower() + trabajador.nombre[:3].lower()

            if password.lower() == expected_password:
                # Si la contraseña es correcta, guarda los datos del trabajador en la sesión
                request.session['trabajador_id'] = trabajador.id
                request.session['trabajador_nombre'] = f"{trabajador.nombre} {trabajador.apellido}"
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect('home')  # Redirige a la página principal
            else:
                # Si la contraseña es incorrecta, muestra un mensaje de error
                messages.error(request, "Credenciales incorrectas.")
        except Trabajador.DoesNotExist:
            # Si el trabajador no existe, muestra un mensaje genérico
            messages.error(request, "Credenciales incorrectas.")
    
    # Renderiza la página de inicio de sesión
    return render(request, 'gestion/login.html')

# Vista para cerrar la sesión de un trabajador.
def logout_trabajador(request):
    """
    Finaliza la sesión del trabajador actual y lo redirige a la página de inicio de sesión.
    """
    logout(request)  # Cierra la sesión
    return redirect('login')  # Redirige al login



# Vista para agregar un nuevo cliente.
def agregar_cliente(request):
    """
    Procesa un formulario para agregar un nuevo cliente a la base de datos.
    Renderiza un formulario en una plantilla HTML externa.
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)  # Instancia el formulario con los datos enviados
        if form.is_valid():
            form.save()  # Guarda el cliente en la base de datos
            return redirect('tabla_clientes')  # Redirige a la página principal
        else:
            # Renderiza la plantilla con los errores
            return render(request, 'gestion/agregar_cliente.html', {'form': form})
    else:
        # Renderiza la plantilla con un formulario vacío
        form = ClienteForm()
        return render(request, 'gestion/agregar_cliente.html', {'form': form})
    
def editar_cliente(request, cliente_id):
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

# Vista para agregar una nueva reserva.
def agregar_reserva(request):
    """
    Procesa un formulario para agregar una nueva reserva a la base de datos.
    Renderiza un formulario en una plantilla HTML externa.
    """
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            # Obtén los datos validados del formulario
            cliente = form.cleaned_data['cliente']
            habitacion = form.cleaned_data['habitacion']
            fecha_ingreso = form.cleaned_data['fecha_ingreso']
            noches = form.cleaned_data['noches']
            fecha_registro = datetime.now()  # Fecha de registro es la fecha actual

            # Calcula el precio final basado en las noches y el precio de la habitación
            precio_final = habitacion.precio * noches

            # Crea la reserva sin guardarla aún
            reserva = form.save(commit=False)
            reserva.precio_final = precio_final
            reserva.estado = "pendiente"
            reserva.fecha_registro = fecha_registro  # Asignamos la fecha de registro
            reserva.save()

            # Actualizamos el estado de la habitación
            habitacion.estado = "reservada"
            habitacion.save()

            messages.success(request, "Reserva agregada correctamente.")
            return redirect('home')
        else:
            # Si el formulario no es válido
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ReservaForm()

    # Filtrar habitaciones disponibles
    habitaciones_disponibles = Habitacion.objects.filter(estado="disponible")
    # Pasar clientes y habitaciones disponibles al contexto si es necesario
    data = {
        'form': form,
        'habitaciones': habitaciones_disponibles,
    }
    
    return render(request, 'gestion/agregar_reserva.html', data)


def editar_reserva(request, pk):
    """
    Permite editar una reserva existente.
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





# Vista para la página principal del sistema.
def home(request):
    """
    Renderiza la página principal.
    """
    # Verificar si el usuario está autenticado
    trabajador_id = request.session.get('trabajador_id')
    if not trabajador_id:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect('login')
    try:
        # Recuperar los datos del trabajador autenticado
        trabajador = Trabajador.objects.get(id=trabajador_id)
    except Trabajador.DoesNotExist:
        # Manejar el caso en que el trabajador no exista en la base de datos
        del request.session['trabajador_id']
        messages.error(request, "Tu sesión no es válida. Por favor, inicia sesión nuevamente.")
        return redirect('login')

    # Recuperar todas las reservas activas (puedes ajustar el filtro si es necesario)
    reservas = Reserva.objects.all()

    # Instanciar formularios vacíos
    cliente_form = ClienteForm()
    reserva_form = ReservaForm()

    # Datos que se enviarán a la plantilla
    data = {
        'trabajador': trabajador,
        'reservas': reservas,
        'cliente_form': cliente_form,
        'reserva_form': reserva_form,
    }

    # Renderizar la plantilla con los datos
    return render(request, 'gestion/home.html', data)

# Vista para mostrar la tabla de clientes.
def tabla_clientes(request):
    """
    Renderiza una tabla con los datos de todos los clientes registrados en el sistema.
    Solo se puede acceder si hay un trabajador autenticado.
    """
    if 'trabajador_id' not in request.session:
        # Si no hay un trabajador autenticado, redirige al login
        return redirect('login')
    
    # Obtiene todos los clientes
    clientes = Cliente.objects.all()
    # Recupera el nombre del trabajador desde la sesión
    trabajador = request.session['trabajador_nombre']
    # Datos que se enviarán a la plantilla
    data = {
        'clientes': clientes,
        'trabajador': trabajador,
    }
    # Renderiza la plantilla con la lista de clientes
    return render(request, 'gestion/clientes.html', data)

# Vista para mostrar la tabla de habitaciones.
def tabla_habitaciones(request):
    """
    Renderiza una tabla con los datos de todas las habitaciones disponibles.
    Solo se puede acceder si hay un trabajador autenticado.
    """
    if 'trabajador_id' not in request.session:
        # Si no hay un trabajador autenticado, redirige al login
        return redirect('login')
    
    # Obtiene todas las habitaciones
    habitaciones = Habitacion.objects.all()
    # Recupera el nombre del trabajador desde la sesión
    trabajador = request.session['trabajador_nombre']
    # Datos que se enviarán a la plantilla
    data = {
        'habitaciones': habitaciones,
        'trabajador': trabajador,
    }
    # Renderiza la plantilla con la lista de habitaciones
    return render(request, 'gestion/habitaciones.html', data)



