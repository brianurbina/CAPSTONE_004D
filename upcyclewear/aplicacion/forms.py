# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class UsuarioRegisterForm(UserCreationForm):
    telefono = forms.CharField(max_length=15, required=False)
    direccion = forms.CharField(max_length=255, required=False)
    fotoperfil = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telefono', 'direccion', 'fotoperfil', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'fotoperfil': forms.FileInput(),
        }

class FundacionRegisterForm(UserCreationForm):
    telefono = forms.CharField(max_length=15, required=False)
    rut = forms.CharField(max_length=12, required=False)
    logotipo = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telefono', 'rut', 'logotipo', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'logotipo': forms.FileInput(),
        }



