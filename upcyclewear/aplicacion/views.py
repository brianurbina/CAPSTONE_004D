from django.shortcuts import render, redirect
from .forms import UsuarioRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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
def donar(request):
    return render(request, 'menuuser/donar.html')

@login_required(login_url='/')
def fundaciones(request):
    return render(request, 'menuuser/fundaciones.html')

@login_required(login_url='/')
def mapa(request):
    return render(request, 'menuuser/mapa.html')

@login_required(login_url='/')
def pedir(request):
    return render(request, 'menuuser/pedir.html')


