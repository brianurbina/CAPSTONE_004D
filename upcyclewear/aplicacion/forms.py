from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Fundacion,Donacion,Peticion
from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import ModelChoiceField
from django.forms.widgets import Widget

class UsuarioRegisterForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=20, required=False)
    foto_perfil = forms.ImageField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'direccion', 'foto_perfil', 'password1', 'password2', 'descripcion']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'foto_perfil': forms.FileInput(),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        user = super().save(commit)
        
        # Cambiar el nombre del archivo de la foto de perfil
        if self.cleaned_data.get('foto_perfil'):
            foto = self.cleaned_data['foto_perfil']
            # Cambia el nombre del archivo
            foto.name = f"{user.username}.jpg"  # O el formato que prefieras
            user.foto_perfil = foto
        
        if commit:
            user.save()
        
        return user





class FundacionForm(forms.ModelForm):

    class Meta: 
        model = Fundacion
        fields = ['rut', 'razon_social', 'comuna', 'region', 'direccion', 'descripcion', 'telefono', 'logotipo', 'sitio_web']
        labels = {
            'rut': 'RUT:',
            'razon_social': 'Razón Social:',
            'comuna': 'Comuna:',
            'region': 'Región:',
            'direccion': 'Dirección:',
            'descripcion': 'Descripción:',
            'telefono': 'Teléfono:',
            'logotipo': 'Logotipo:',
            'sitio_web': 'Sitio Web:',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RUT', 'id': 'rut'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la razón social', 'id': 'razon_social'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la comuna', 'id': 'comuna'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la región', 'id': 'region'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección', 'id': 'direccion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono', 'id': 'telefono'}),
            'logotipo': forms.FileInput(attrs={'class': 'file-input', 'id': 'logotipo', 'style': 'color: white; background-color: green; text-align: center; width: 100%;'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el sitio web', 'id': 'sitio_web'}),
        }

    def save(self, commit=True):
        # Crear una instancia sin guardar
        fundacion = super().save(commit=False)
        # Establecer 'aprobada' como False
        fundacion.aprobada = False
        if commit:
            fundacion.save()
        return fundacion





class PeticionForm(forms.ModelForm):

    class Meta:
        model = Peticion
        fields = ['titulo', 'tipo_ropa', 'descripcion']  # Eliminar 'id'
        labels = {
            'titulo': 'Título:',
            'tipo_ropa': 'Tipo de Ropa:',
            'descripcion': 'Descripción:',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título', 'id': 'titulo'}),
            'tipo_ropa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el tipo de ropa', 'id': 'tipo_ropa'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
        }

    def save(self, commit=True):
        peticion = super().save(commit=False)
        peticion.estado = 'activa'  # Establecer estado como 'activa' por defecto
        return peticion  # Retornamos el objeto para que se guarde en la vista


from django import forms
from .models import Donacion

class DonacionForm(forms.ModelForm):

    class Meta:
        model = Donacion
        fields = ['titulo', 'tipo_ropa', 'talla', 'temporada', 'descripcion', 'foto']  # Eliminar 'id'
        labels = {
            'titulo': 'Título:',
            'tipo_ropa': 'Tipo de Ropa:',
            'talla': 'Talla:',
            'temporada': 'Temporada:',
            'descripcion': 'Descripción:',
            'foto': 'Foto:',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título', 'id': 'titulo'}),
            'tipo_ropa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el tipo de ropa', 'id': 'tipo_ropa'}),
            'talla': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la talla', 'id': 'talla'}),
            'temporada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la temporada', 'id': 'temporada'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'file-input', 'id': 'foto', 'style': 'color: white; background-color: green; text-align: center; width: 100%;'}),
        }

    def save(self, commit=True):
        donacion = super().save(commit=False)
        donacion.estado = 'disponible'  # Establecer estado como 'disponible' por defecto
        return donacion  # Retornamos el objeto para que se guarde en la vista
