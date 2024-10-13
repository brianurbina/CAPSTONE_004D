from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Usuario, Fundacion, Peticion, Donacion
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.core.paginator import Paginator

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
def chat(request):
    return render(request, 'menuuser/chat.html')





@login_required(login_url='/')
def pedir(request):
    return render(request, 'menuuser/pedir.html')




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
