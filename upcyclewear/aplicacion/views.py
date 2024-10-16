from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioRegisterForm, FundacionForm, PeticionForm, DonacionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Usuario, Fundacion, Peticion, Donacion, Conversacion, Mensaje
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MensajeSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import random
import string
from datetime import datetime
import pytz
import uuid
# Create your views here.


@login_required(login_url='/')
def index(request):
    return render(request, 'index.html')


def principal(request):
    # Si el usuario ya está autenticado, lo redirigimos al 'index'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        # Capturamos el username (email en este caso) y password del formulario
        email = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticamos al usuario con los datos ingresados
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Si la autenticación es exitosa, iniciamos sesión y redirigimos
            login(request, user)
            messages.success(request, '¡Has iniciado sesión correctamente!')
            return redirect('index')
        else:
            # Si la autenticación falla, mostramos el mensaje de error
            messages.error(request, 'Ups! Al parecer te equivocaste en tu usuario o contraseña.')

    # Enviamos la página de login (principal.html)
    return render(request, 'principal.html')


def register(request):
    if request.method == 'POST':
        form = UsuarioRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'usuario'
            user.save()
            login(request, user)
            return redirect('principal')
    else:
        form = UsuarioRegisterForm()
    return render(request, 'register/register.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirige al usuario a una página después de cerrar sesión (opcional)
    return redirect('/')  # Reemplaza 'inicio' con el nombre de tu URL



#VISTAS USUARIO:


@login_required(login_url='/')
def pedir(request):
    # Obtener todas las donaciones del usuario actual
    donaciones = Donacion.objects.all().order_by('-fecha_hora')  # Ordenar por fecha, de más reciente a más antiguo

    # Paginación (opcional)
    from django.core.paginator import Paginator
    paginator = Paginator(donaciones, 10)  # Mostrar 10 donaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con las donaciones
    return render(request, 'menuuser/pedir.html', {
        'donaciones': page_obj
    })


#VISTAS PERFILES

@login_required(login_url='/')
def mi_perfil(request):
    return render(request, 'perfil/mi_perfil.html')


@login_required(login_url='/')
def perfil_usuario(request, username):
    usuario = get_object_or_404(Usuario, username=username)
    return render(request, 'perfil/perfil_usuario.html', {'usuario': usuario})






#Vistas Fundación
@login_required(login_url='/')
def fundaciones(request):
    query = request.GET.get('q')  # Obtener la búsqueda del usuario
    if query:
        foundations = Fundacion.objects.filter(
            Q(razon_social__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(comuna__icontains=query) |
            Q(region__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query)
        )
    else:
        foundations = Fundacion.objects.all()  # Obtener todas las fundaciones si no hay búsqueda

    return render(request, 'menuuser/fundaciones.html', {'foundations': foundations})
    
##class FundacionDetailView(DetailView):
  #  model = Fundacion
   # template_name = 'fundacion_detail.html'


@login_required(login_url='/')
def donar(request): 
    query = request.GET.get('q')  # Obtener la búsqueda del usuario
    if query:
        peticiones = Peticion.objects.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(tipo_ropa__icontains=query) |
            Q(usuario__username__icontains=query)
        )
    else:
        peticiones = Peticion.objects.all()  # Obtener todas las peticiones si no hay búsqueda

    # Paginación
    paginator = Paginator(peticiones, 10)  # 10 peticiones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'menuuser/donar.html', {'peticiones': page_obj})




#VISTAS MAPA
@login_required(login_url='/')
def mapa(request):
    query = request.GET.get('q')  # Obtener la búsqueda del usuario
    if query:
        foundations = Fundacion.objects.filter(
            Q(razon_social__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(comuna__icontains=query) |
            Q(region__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query)
        )
    else:
        foundations = Fundacion.objects.all()  # Obtener todas las fundaciones si no hay búsqueda
    return render(request, 'menuuser/mapa.html', {'foundations': foundations})





#CHAT


@login_required(login_url='/')
def ver_conversacion(request):
    # Obtener todas las conversaciones del usuario
    conversaciones = Conversacion.objects.filter(usuario1=request.user) | Conversacion.objects.filter(usuario2=request.user)

    # Obtener la conversación seleccionada si existe
    selected_conversacion_id = request.GET.get('conversacion_id')
    selected_conversacion = None
    mensajes = []

    if selected_conversacion_id:
        selected_conversacion = get_object_or_404(Conversacion, id_conversacion=selected_conversacion_id)
        mensajes = selected_conversacion.mensajes.all()

        # Convertir la fecha y hora a hora chilena si no se hizo en el guardado
        for mensaje in mensajes:
            mensaje.fecha_hora = mensaje.fecha_hora.astimezone(pytz.timezone('America/Santiago'))

    return render(request, 'menuuser/conversaciones.html', {
        'conversaciones': conversaciones,
        'selected_conversacion': selected_conversacion,
        'mensajes': mensajes,
    })

from datetime import datetime
import pytz

@login_required
def guardar_mensaje(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mensaje_texto = data.get('mensaje')
        conversacion_id = data.get('conversacion_id')

        print(f"Mensaje recibido: {mensaje_texto}, Conversación ID: {conversacion_id}")

        # Obtener la conversación o devolver un 404 si no existe
        conversacion = get_object_or_404(Conversacion, id_conversacion=conversacion_id)

        # Generar un ID único para el mensaje
        id_mensaje = str(uuid.uuid4())
        print(f"Generando ID de mensaje: {id_mensaje}")

        # Obtener la hora actual en la zona horaria de Chile
        hora_actual_chilena = datetime.now(pytz.timezone('America/Santiago'))

        # Crear y guardar el mensaje
        mensaje = Mensaje(
            id_mensaje=id_mensaje,
            mensaje=mensaje_texto,
            emisor=request.user,
            conversacion=conversacion,
            fecha_hora=hora_actual_chilena  # Asignar la hora chilena
        )
        mensaje.save()
        print("Mensaje guardado en la base de datos.")

        # Devolver la respuesta en formato JSON
        return JsonResponse({
            'emisor': request.user.username,
            'mensaje': mensaje_texto,
            'fecha_hora': hora_actual_chilena.isoformat()  # Devolver la hora también
        }, status=201)

    print("Método no permitido.")
    return JsonResponse({'error': 'Método no permitido'}, status=405)



@login_required
def crear_conversacion(request, usuario_username):
    try:
        usuario2 = get_object_or_404(Usuario, username=usuario_username)
        conversacion = Conversacion.objects.filter(
            (Q(usuario1=request.user) & Q(usuario2=usuario2)) |
            (Q(usuario1=usuario2) & Q(usuario2=request.user))
        ).first()

        if not conversacion:
            id_conversacion = ''.join(random.choices('123456789', k=13))
            conversacion = Conversacion(
                id_conversacion=id_conversacion,
                usuario1=request.user,
                usuario2=usuario2
            )
            conversacion.save()

        return JsonResponse({'conversacion_id': conversacion.id_conversacion})

    except Exception as e:
        print(f"Error al crear la conversación: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)





#FORMULARIOS
def crear_fundacion(request):
    if request.method == 'POST':
        form = FundacionForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES para manejar archivos
        if form.is_valid():
            form.save()  # Guardar el formulario
            return redirect('fundaciones')  # Redirigir a la lista de fundaciones (cambia según tu URL)
    else:
        form = FundacionForm()

    return render(request, 'forms/form_fundacion.html', {'form': form})


import uuid
from django.shortcuts import render, redirect
from .forms import PeticionForm
from .models import Peticion

def crear_peticion(request):
    if request.method == 'POST':
        form = PeticionForm(request.POST, request.FILES)
        if form.is_valid():
            peticion = form.save(commit=False)  # No guardar aún
            peticion.id = str(uuid.uuid4())  # Generar un nuevo ID
            peticion.estado = 'activa'  # Establecer estado como 'activa'
            peticion.usuario = request.user  # Asignar el usuario actual
            peticion.receptor = request.user  # Asignar el receptor si es necesario
            peticion.save()  # Guardar la instancia
            return redirect('donar')  # Cambia según tu URL
    else:
        form = PeticionForm()

    return render(request, 'forms/form_peticion.html', {'form': form})

def crear_donacion(request):
    if request.method == 'POST':
        form = DonacionForm(request.POST, request.FILES)
        if form.is_valid():
            donacion = form.save(commit=False)  # No guardar aún
            donacion.id = str(uuid.uuid4())  # Generar un nuevo ID
            donacion.estado = 'disponible'  # Establecer estado como 'disponible'
            donacion.donador = request.user  # Asignar el usuario actual como donador
            donacion.usuario = request.user  # Asignar el usuario actual (si este es el campo que necesitas)
            donacion.save()  # Guardar la instancia
            return redirect('pedir')  # Cambia según tu URL
    else:
        form = DonacionForm()

    return render(request, 'forms/form_donacion.html', {'form': form})