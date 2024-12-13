from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Fundacion,Donacion,Peticion, Reseña, ReporteUsuario
from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import ModelChoiceField
from django.forms.widgets import Widget

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario  # Asegúrate de que la ruta de importación sea correcta

class UsuarioRegisterForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    foto_perfil = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name','username', 'email', 'telefono', 'direccion', 'foto_perfil', 'password1', 'password2', 'descripcion']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
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



from django import forms
from .models import Fundacion

class FundacionForm(forms.ModelForm):
    class Meta: 
        model = Fundacion
        fields = ['rut', 'razon_social', 'comuna_region', 'direccion', 'descripcion', 'telefono', 'logotipo', 'sitio_web']
        labels = {
            'rut': 'RUT:',
            'razon_social': 'Razón Social:',
            'comuna_region': 'Comuna:',
            'direccion': 'Dirección:',
            'descripcion': 'Descripción:',
            'telefono': 'Teléfono:',
            'logotipo': 'Logotipo:',
            'sitio_web': 'Sitio Web:',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RUT', 'id': 'rut'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la razón social', 'id': 'razon_social'}),
            'comuna_region': forms.Select(
                choices=[('', 'Selecciona una comuna')] + Fundacion.REGIONES_Y_COMUNAS,
                attrs={'class': 'form-control', 'id': 'comuna_region'}
            ),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección', 'id': 'direccion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono', 'id': 'telefono'}),
            'logotipo': forms.FileInput(attrs={'class': 'file-input', 'id': 'logotipo', 'style': 'color: white; background-color: green; text-align: center; width: 100%;'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el sitio web', 'id': 'sitio_web'}),
        }

    # Establecer valor por defecto para comuna_region
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna_region'].initial = ''  # Valor predeterminado vacío

        

    def save(self, commit=True):
        # Crear una instancia sin guardar
        fundacion = super().save(commit=False)
        # Establecer 'aprobada' como False
        fundacion.aprobada = False
        if commit:
            fundacion.save()
        return fundacion
    
class FundacionFormMod(forms.ModelForm):

    class Meta: 
        model = Fundacion
        fields = ['rut', 'razon_social', 'comuna_region', 'direccion', 'descripcion', 'telefono', 'logotipo', 'sitio_web','aprobada']
        labels = {
            'rut': 'RUT:',
            'razon_social': 'Razón Social:',
            'comuna_region': 'Comuna:',
            'direccion': 'Dirección:',
            'descripcion': 'Descripción:',
            'telefono': 'Teléfono:',
            'logotipo': 'Logotipo:',
            'sitio_web': 'Sitio Web:',
            'aprobada': 'Aprobada',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RUT', 'id': 'rut'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la razón social', 'id': 'razon_social'}),
            'comuna_region': forms.Select(choices=Fundacion.REGIONES_Y_COMUNAS, attrs={'class': 'form-control', 'id': 'comuna_region'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección', 'id': 'direccion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono', 'id': 'telefono'}),
            'logotipo': forms.FileInput(attrs={'class': 'file-input', 'id': 'logotipo', 'style': 'color: white; background-color: green; text-align: center; width: 100%;'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el sitio web', 'id': 'sitio_web'}),
            'aprobada': forms.CheckboxInput(),
        }




class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ['titulo', 
                  'tipo_ropa', 
                  #'talla',
                  'descripcion']  # Asegúrate de incluir 'talla' también
                  #'estado',
        labels = {
            'titulo': 'Título:',
            'tipo_ropa': 'Tipo de Ropa:',
            #'talla': 'Talla:',  # Asegúrate de agregar la etiqueta para talla
            'descripcion': 'Descripción:',
            #'estado': 'Estado:',  # Agregado etiqueta para 'estado'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título', 'id': 'titulo'}),
            'tipo_ropa': forms.Select(choices=Peticion.TIPO_ROPA_CHOICES, attrs={'class': 'form-control', 'placeholder': 'Seleccione el tipo de ropa', 'id': 'tipo_ropa'}),  # Cambiado a Select
            #'talla': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione la talla', 'id': 'talla'}),  # Añadir widget para 'talla'
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
            #'estado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ingrese el estado', 'id': 'estado'}),  # Añadir widget para 'estado'
        }

    def save(self, commit=True):
        peticion = super().save(commit=False)
        peticion.estado = 'activa'  # Establecer estado como 'activa' por defecto
        if commit:
            peticion.save()  # Guardar la petición si commit es True
        return peticion #retomamos objeto para que se guarde


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
            'tipo_ropa': forms.Select(choices=Donacion.TIPO_ROPA_CHOICES ,attrs={
                'class': 'form-control',
                'id': 'tipo_ropa',
                'placeholder': 'Indica el tipo de ropa'
            },),
            'temporada': forms.Select(choices=Donacion.TEMPORADAS ,attrs={
                'class': 'form-control',
                'id': 'temporada',
                'placeholder': 'Indica la temporada'}),
            'talla': forms.Select(choices=Donacion.TALLAS ,attrs={
                'class': 'form-control',
                'id': 'talla',
                'placeholder': 'Indica la talla'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'file-input', 'id': 'foto', 'style': 'color: white; background-color: green; text-align: center; width: 100%;'}),
        }

    def save(self, commit=True):
        donacion = super().save(commit=False)
        donacion.estado = 'disponible'  # Establecer estado como 'disponible' por defecto
        return donacion  # Retornamos el objeto para que se guarde en la vista





class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['estrellas', 'reseña']  # Incluye los campos que quieras en el formulario
        widgets = {
            'reseña': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe aquí tu reseña...', 'rows': 4}),
        }

    def clean_reseña(self):
        reseña = self.cleaned_data.get('reseña')
        if not reseña:  # Si el campo está vacío
            return "Sin Descripción..."  # Devuelve el valor por defecto
        return reseña  # Devuelve el valor ingresado si no está vacío


class ReporteUsuarioForm(forms.ModelForm):
    class Meta:
        model = ReporteUsuario
        fields = ['motivo', 'descripcion']  # Asegúrate de incluir el motivo y la descripción
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripción del motivo...', 'rows': 4}),
        }




class PeticionFormMod(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ['titulo','usuario' ,'tipo_ropa', 'descripcion', 'estado', 'donador']
        
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'titulo',
                'placeholder': 'Escribe el título de la petición'
            }),
            'tipo_ropa': forms.Select(choices=Peticion.TIPO_ROPA_CHOICES,attrs={
                'class': 'form-control',
                'id': 'tipo_ropa',
                'placeholder': 'Indica el tipo de ropa'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'descripcion',
                'placeholder': 'Descripción de la petición'
            }),
            'estado': forms.Select(choices=Peticion.ESTADO_CHOICES, attrs={
                'class': 'form-control',
                'id': 'estado'
            })
            ,
            'usuario': forms.Select(attrs={
                'class': 'form-control',
                'id': 'usuario'
            }),
            'donador': forms.Select(attrs={
                'class': 'form-control',
                'id': 'donador'
            }),
        }


from django import forms
from .models import Donacion, Usuario

class DonacionFormMod(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = [
            'id',          # Añadimos el campo ID
            'usuario',     # Añadimos el campo Usuario
            'titulo',
            'tipo_ropa',
            'talla',
            'temporada',
            'descripcion',
            'foto',
            'estado',
            'receptor'
        ]
        labels = {
            'id': 'ID',
            'usuario': 'Usuario',
            'titulo': 'Título',
            'tipo_ropa': 'Tipo de Ropa',
            'talla': 'Talla',
            'temporada': 'Temporada',
            'descripcion': 'Descripción',
            'foto': 'Foto',
            'estado': 'Estado',
            'receptor': 'Receptor'
        }
        widgets = {
            'estado': forms.Select(choices=Donacion.ESTADO_CHOICES),
            'receptor': forms.Select(),
            'tipo_ropa': forms.Select(choices=Donacion.TIPO_ROPA_CHOICES ,attrs={
                'class': 'form-control',
                'id': 'tipo_ropa',
                'placeholder': 'Indica el tipo de ropa'
            },),
            'temporada': forms.Select(choices=Donacion.TEMPORADAS ,attrs={
                'class': 'form-control',
                'id': 'temporada',
                'placeholder': 'Indica la temporada'}),
            'talla': forms.Select(choices=Donacion.TALLAS ,attrs={
                'class': 'form-control',
                'id': 'talla',
                'placeholder': 'Indica la talla'})
        
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receptor'].queryset = Usuario.objects.filter(is_active=True)
        self.fields['id'].widget.attrs['readonly'] = True
        self.fields['usuario'].queryset = Usuario.objects.all()

        # Hacer que ciertos campos sean opcionales
        self.fields['foto'].required = False  # Campo opcional
        self.fields['receptor'].required = False  # Campo opcional
    


from django import forms
from .models import Fundacion

class FiltroFundacionForm(forms.Form):
    # Agregamos la opción 'TODOS' al principio y eliminamos 'Seleccione una opción'
    comuna_region = forms.ChoiceField(
        choices=[('TODOS', 'Todos')] + Fundacion.REGIONES_Y_COMUNAS,  # Agregar 'TODOS' al principio
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'comuna_region'})
    )
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar...', 'id': 'query'})
    )