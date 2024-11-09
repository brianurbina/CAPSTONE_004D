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





# Listado de comunas
COMUNA_CHOICES = [
    ('', 'Seleccione una comuna'),  # Valor inicial vacío
    ('Santiago', 'Santiago'),
    ('Maipú', 'Maipú'),
    ('La Florida', 'La Florida'),
    ('Cerrillos', 'Cerrillos'),
    ('Lo Barnechea', 'Lo Barnechea'),
    ('San Joaquín', 'San Joaquín'),
    ('Estación Central', 'Estación Central'),
    ('San Bernardo', 'San Bernardo'),
    ('San José de Mayo', 'San José de Mayo'),
    ('San Pedro de Atacama', 'San Pedro de Atacama'),
    ('Chillán', 'Chillán'),
    ('Los Angeles', 'Los Angeles'),
    ('Talca', 'Talca'),
    ('Chillán Viejo', 'Chillán Viejo'),
    ('Llanquihue', 'Llanquihue'),
    ('Osorno', 'Osorno'),
    ('Palena', 'Palena'),
    ('San Juan de la Costa', 'San Juan de la Costa'),
    ('Concepción', 'Concepción'),
    ('Arauco', 'Arauco'),
    ('Huasco', 'Huasco'),
    ('Cautín', 'Cautín'),
    ('Malleco', 'Malleco'),
    ('Yumbel', 'Yumbel'),
    ('Lonquimay', 'Lonquimay'),
    ('Alto Hospicio', 'Alto Hospicio'),
    ('San Pedro de la Paz', 'San Pedro de la Paz'),
    ('Nuble', 'Nuble'),
    ('San Vicente de Tagua Tagua', 'San Vicente de Tagua Tagua'),
    ('Chiloe', 'Chiloe'),
    ('San Antonio', 'San Antonio'),
    ('Talagante', 'Talagante'),
    ('Chimborazo', 'Chimborazo'),
    ('San José de la Montaña', 'San José de la Montaña'),
    ('San Luis de la Paz', 'San Luis de la Paz'),
    ('Teno', 'Teno'),
    ('Vilcún', 'Vilcún'),
    ('San José de Uraco', 'San José de Uraco'),
    ('San Pedro de los Milagros', 'San Pedro de los Milagros'),
    ('San Fernando', 'San Fernando'),
    ('Tapachello', 'Tapachello'),
    ('Chimichagua', 'Chimichagua'),
    ('Ocotillo', 'Ocotillo'),
    ('San Vicente de Chuco', 'San Vicente de Chuco'),
    ('Peralillo', 'Peralillo'),
    ('Pichilemu', 'Pichilemu'),
    ('La Ligua', 'La Ligua'),
    ('Colchagua', 'Colchagua'),
    ('San Cristóbal', 'San Cristóbal'),
    ('Castro', 'Castro'),
    ('Las Cortes', 'Las Cortes'),
    ('Quillón', 'Quillón'),
    ('San José de Siguas', 'San José de Siguas'),
    ('San Antonio de los Andes', 'San Antonio de los Andes'),
    ('San Gabriel', 'San Gabriel'),
    ('Natales', 'Natales'),
    ('San José de las Lajas', 'San José de las Lajas'),
    ('Talcahuano', 'Talcahuano'),
    ('Curicó', 'Curicó'),
    ('Talamanca', 'Talamanca'),
    ('Chillán de los Chaves', 'Chillán de los Chaves'),
    ('Santa Cruz', 'Santa Cruz'),
    ('Litueche', 'Litueche'),
    ('Chiloe de los Santos', 'Chiloe de los Santos'),
    ('Parral', 'Parral'),
    ('San Felipe', 'San Felipe'),
    ('San José de la Montaña', 'San José de la Montaña'),
    ('San Pedro de la Costa', 'San Pedro de la Costa'),
    ('Chimbarongo', 'Chimbarongo'),
    ('San José de la Maguana', 'San José de la Maguana'),
    ('San Pedro de la Paz', 'San Pedro de la Paz'),
    ('San Fernando de Apure', 'San Fernando de Apure'),
    ('San Clemente', 'San Clemente'),
    ('Santa Elena', 'Santa Elena'),
    ('San Carlos', 'San Carlos'),
    ('San Miguel', 'San Miguel'),
    ('Tambolón', 'Tambolón'),
    ('Villa Alegre', 'Villa Alegre'),
    ('Villa de Castro', 'Villa de Castro'),
    ('Hualañé', 'Hualañé'),
    ('Nacimiento', 'Nacimiento'),
    ('Parral', 'Parral'),
    ('San Pedro de la Paz', 'San Pedro de la Paz'),
    ('San Fernando de Vallecas', 'San Fernando de Vallecas'),
    ('San José de la Mari', 'San José de la Mari'),
    ('San Luis de la Paz', 'San Luis de la Paz'),
    ('San Miguel de Tucumán', 'San Miguel de Tucumán'),
    ('Temuco', 'Temuco'),
    ('Quillota', 'Quillota'),
    ('La Serena', 'La Serena'),
    ('Concepción', 'Concepción'),
    ('Talca', 'Talca'),
    ('Chillán', 'Chillán'),
    ('La Ligua', 'La Ligua'),
    ('Colchagua', 'Colchagua'),
    ('San Cristóbal', 'San Cristóbal'),
    ('Castro', 'Castro'),
    ('Las Cortes', 'Las Cortes'),
    ('Quillón', 'Quillón'),
    ('San José de Siguas', 'San José de Siguas'),
    ('San Antonio de los Andes', 'San Antonio de los Andes'),
    ('San Gabriel', 'San Gabriel'),
    ('Natales', 'Natales'),
]

"""REGIONS_CHOICES = [
    ("I - Tarapacá", "I - Tarapacá"),
    ("II - Antofagasta", "II - Antofagasta"),
    ("III - Atacama", "III - Atacama"),
    ("IV - Coquimbo", "IV - Coquimbo"),
    ("V - Valparaíso", "V - Valparaíso"),
    ("VI - O’Higgins", "VI - O’Higgins"),
    ("VII - Maule", "VII - Maule"),
    ("VIII - Biobío", "VIII - Biobío"),
    ("IX - Araucanía", "IX - Araucanía"),
    ("X - Los Lagos", "X - Los Lagos"),
    ("XI - Aisén", "XI - Aisén"),
    ("XII - Magallanes", "XII - Magallanes"),
    ("XIII - Metropolitana de Santiago", "XIII - Metropolitana de Santiago"),
    ("XIV - Los Ríos", "XIV - Los Ríos"),
    ("XV - Arica y Parinacota", "XV - Arica y Parinacota"),
    ("XVI - Ñuble", "XVI - Ñuble"),
]"""
REGIONS_CHOICES = [
    ("Arica y Parinacota", "Región de Arica y Parinacota"),
    ("Tarapacá", "Región de Tarapacá"),
    ("Antofagasta", "Región de Antofagasta"),
    ("Atacama", "Región de Atacama"),
    ("Coquimbo", "Región de Coquimbo"),
    ("Valparaíso", "Región de Valparaíso"),
    ("Metropolitana de Santiago", "Región Metropolitana"),
    ("O’Higgins", "Región del Libertador General Bernardo O’Higgins"),
    ("Maule", "Región del Maule"),
    ("Ñuble", "Región de Ñuble"),
    ("Biobío", "Región del Biobío"),
    ("La Araucanía", "Región de La Araucanía"),
    ("Los Ríos", "Región de Los Ríos"),
    ("Los Lagos", "Región de Los Lagos"),
    ("Aysén", "Región de Aysén del General Carlos Ibáñez del Campo"),
    ("Magallanes", "Región de Magallanes y de la Antártica Chilena")
]


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
            'comuna': forms.Select(choices=COMUNA_CHOICES, attrs={'class': 'form-control', 'id': 'comuna'}),
            'region': forms.Select(choices=REGIONS_CHOICES, attrs={'class': 'form-control', 'id': 'region'}),
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
    
class FundacionFormMod(forms.ModelForm):

    class Meta: 
        model = Fundacion
        fields = ['rut', 'razon_social', 'comuna', 'region', 'direccion', 'descripcion', 'telefono', 'logotipo', 'sitio_web','aprobada']
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
            'aprobada': 'Aprobada',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RUT', 'id': 'rut'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la razón social', 'id': 'razon_social'}),
            'comuna': forms.Select(choices=COMUNA_CHOICES, attrs={'class': 'form-control', 'id': 'comuna'}),
            'region': forms.Select(choices=REGIONS_CHOICES, attrs={'class': 'form-control', 'id': 'region'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección', 'id': 'direccion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción', 'id': 'descripcion', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono', 'id': 'telefono'}),
            'logotipo': forms.FileInput(attrs={'class': 'file-input', 'id': 'logotipo', 'style': 'color: white; background-color: green; text-align: center; width: 100%;'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el sitio web', 'id': 'sitio_web'}),
            'aprobada': forms.CheckboxInput(),
        }



# Definimos las opciones para el campo tipo_ropa
TIPO_ROPA_CHOICES = [
    ('', 'Seleccione una opción'),  # Opción por defecto
    # Ropa Superior
    ('Ropa Superior', [
        ('camiseta', 'Camiseta'),
        ('polo', 'Polo'),
        ('blusa', 'Blusa'),
        ('camisa', 'Camisa'),
        ('top', 'Top'),
        ('sueter', 'Suéter'),
        ('sudadera', 'Sudadera'),
        ('chaqueta', 'Chaqueta'),
        ('abrigo', 'Abrigo'),
        ('cardigan', 'Cárdigan'),
        ('chaleco', 'Chaleco'),
        ('camiseta_sin_mangas', 'Camiseta sin mangas'),
        ('blazer', 'Saco o Blazer'),
        ('jersey', 'Jersey'),
    ]),
    # Ropa Inferior
    ('Ropa Inferior', [
        ('pantalon', 'Pantalón'),
        ('falda', 'Falda'),
        ('shorts', 'Shorts'),
        ('bermudas', 'Bermudas'),
        ('leggings', 'Leggings'),
        ('capris', 'Capris'),
    ]),
    # Vestidos
    ('Vestidos', [
        ('vestido_fiesta', 'Vestido de Fiesta'),
        ('vestido_casual', 'Vestido Casual'),
        ('vestido_noche', 'Vestido de Noche'),
        ('vestido_largo', 'Vestido Largo'),
        ('vestido_corto', 'Vestido Corto'),
        ('vestido_coctel', 'Vestido de Cóctel'),
        ('maxi_vestido', 'Maxi Vestido'),
    ]),
    # Ropa Íntima
    ('Ropa Íntima', [
        ('sujetador', 'Sujetador'),
        ('calzoncillos', 'Calzoncillos'),
        ('bragas', 'Bragas'),
        ('bodysuit', 'Bodysuit'),
        ('camiseta_interior', 'Camiseta interior'),
        ('faja', 'Faja'),
        ('corset', 'Corset'),
        ('camison', 'Camisón'),
        ('pijama', 'Pijamas'),
        ('batas_dormir', 'Batas de dormir'),
    ]),
    # Ropa de Exterior
    ('Ropa de Exterior', [
        ('abrigo', 'Abrigo'),
        ('chaqueta', 'Chaqueta'),
        ('gabardina', 'Gabardina o Trench'),
        ('parka', 'Parka'),
        ('poncho', 'Poncho'),
        ('capa', 'Capa'),
        ('impermeable', 'Impermeable'),
        ('chaleco_acolchado', 'Chaleco acolchado'),
    ]),
    # Ropa Deportiva
    ('Ropa Deportiva', [
        ('sudadera', 'Sudadera'),
        ('pantalon_deportivo', 'Pantalón deportivo'),
        ('shorts_deportivos', 'Shorts deportivos'),
        ('leggings_deportivos', 'Leggings deportivos'),
        ('top_deportivo', 'Top deportivo'),
        ('traje_bano', 'Traje de baño'),
        ('bikini', 'Bikini'),
        ('ropa_ciclismo', 'Ropa de ciclismo'),
        ('ropa_yoga', 'Ropa de yoga'),
    ]),
    # Ropa de Bebé
    ('Ropa de Bebé', [
        ('body', 'Body'),
        ('pelele', 'Pelele'),
        ('mameluco', 'Mameluco'),
        ('babero', 'Babero'),
        ('pantalones_bebe', 'Pantalones para bebé'),
        ('conjuntos_bebe', 'Conjuntos'),
        ('polainas', 'Polainas'),
        ('pijamas_bebe', 'Pijamas para bebé'),
        ('chaleco_acolchado_bebe', 'Chaleco acolchado para bebé'),
    ]),
    # Trajes
    ('Trajes', [
        ('traje_dos_piezas', 'Traje de dos piezas'),
        ('esmoquin', 'Esmoquin'),
        ('traje_tres_piezas', 'Traje de tres piezas'),
        ('conjunto_falda', 'Conjunto de falda y chaqueta'),
        ('conjunto_pantalon', 'Conjunto de pantalón y top'),
    ]),
    # Accesorios de Ropa
    ('Accesorios de Ropa', [
        ('bufanda', 'Bufanda'),
        ('guantes', 'Guantes'),
        ('sombrero', 'Sombrero'),
        ('cinturon', 'Cinturón'),
        ('panuelo', 'Pañuelo'),
        ('calcetines', 'Calcetines'),
        ('ligas', 'Ligas'),
        ('chal', 'Chal'),
    ]),
    # Uniformes
    ('Uniformes', [
        ('uniforme_escolar', 'Uniforme escolar'),
        ('uniforme_trabajo', 'Uniforme de trabajo'),
        ('ropa_enfermeria', 'Ropa de enfermería'),
        ('uniforme_deportivo', 'Uniforme deportivo'),
        ('traje_proteccion', 'Traje de protección'),
        ('uniforme_militar', 'Uniforme militar'),
    ]),
    # Trajes Tradicionales
    ('Trajes Tradicionales', [
        ('kimono', 'Kimono'),
        ('sari', 'Sari'),
        ('traje_folclorico', 'Traje folclórico'),
        ('traje_flamenco', 'Traje de flamenco'),
        ('traje_charro', 'Traje charro'),
        ('toga', 'Toga'),
    ]),
    # Ropa Especializada
    ('Ropa Especializada', [
        ('ropa_maternidad', 'Ropa de maternidad'),
        ('ropa_seguridad', 'Ropa de seguridad'),
        ('ropa_lluvia', 'Ropa de lluvia'),
        ('traje_nieve', 'Traje de nieve'),
        ('traje_neopreno', 'Traje de neopreno'),
    ]),
]

class PeticionForm(forms.ModelForm):
    tipo_ropa = forms.ChoiceField(
        choices=TIPO_ROPA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Ropa',
    )
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
            'tipo_ropa': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el tipo de ropa', 'id': 'tipo_ropa'}),  # Cambiado a Select
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



class PeticionForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = ['id', 'titulo', 'tipo_ropa', 'descripcion', 'estado', 'donador']
        labels = {
            'id': 'ID:',
            'titulo': 'Título:',
            'tipo_ropa': 'Tipo de Ropa:',
            'descripcion': 'Descripción:',
            'estado': 'Estado:',
            'donador': 'Donador:',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el ID', 'id': 'id'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título de la petición', 'id': 'titulo'}),
            'tipo_ropa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el tipo de ropa', 'id': 'tipo_ropa'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese una descripción detallada', 'id': 'descripcion', 'rows': 3}),
            'estado': forms.Select(choices=Peticion.ESTADO_CHOICES, attrs={'class': 'form-control', 'id': 'estado'}),
            'donador': forms.Select(attrs={'class': 'form-control', 'id': 'donador'}),
        }
