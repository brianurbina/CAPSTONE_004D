from django.shortcuts import render, redirect
from .forms import UsuarioRegisterForm, FundacionRegisterForm,CustomAuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

#template cuando el usuario ya esta logeado
def index(request):
    return render(request, 'index.html')

def principal(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirige si el usuario ya está autenticado

    return render(request, 'principal.html')




def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Autenticación con email
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige después del inicio de sesión
            else:
                # Error en la autenticación
                return render(request, 'principal.html', {'form': form, 'error': 'Credenciales incorrectas'})
        else:
            # Error en la validación del formulario
            return render(request, 'principal.html', {'form': form, 'error': 'Formulario inválido'})
    else:
        form = CustomAuthenticationForm()

    return render(request, 'principal.html', {'form': form})




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

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '¡Te haz logeado correctamente!')
                return redirect('home')  # Redirige a la página principal después del login
            else:
                messages.error(request, 'Correo o contraseña invalidos')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'register/login.html', {'form': form})
