from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioRegisterForm, FundacionForm, PeticionForm, DonacionForm, FundacionFormMod, ReseñaForm, ReporteUsuarioForm, PeticionFormMod, DonacionFormMod
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Usuario, Fundacion, Peticion, Donacion, Conversacion, Mensaje, Reseña, ReporteUsuario,Notificacion
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import uuid
import random
import string
from datetime import datetime
import pytz
import uuid

# Create your views here.

# Decorador para verificar si el usuario es superusuario
def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)

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


from .forms import FiltroPedir
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Donacion

@login_required(login_url='/')
def pedir(request):
    form = FiltroPedir(request.GET or None)
    # Obtener parámetros de búsqueda y filtros
    query = request.GET.get('q', '')  # Búsqueda del usuario, por defecto vacío
    tipo_ropa = request.GET.get('tipo_ropa', 'TODOS')
    talla = request.GET.get('talla', '')
    temporada = request.GET.get('temporada', '')

    # Obtener todas las donaciones y aplicar filtros
    if form.is_valid():
        tipo_ropa = form.cleaned_data.get('tipo_ropa')

    donaciones = Donacion.objects.filter(estado='activa')  # Filtrar por estado "activa"

    if tipo_ropa != 'TODOS':
        donaciones = donaciones.filter(tipo_ropa=tipo_ropa)
    if talla:
        donaciones = donaciones.filter(talla=talla)
    if temporada:
        donaciones = donaciones.filter(temporada=temporada)
    
    # Aplicar la búsqueda
    if query:
        donaciones = donaciones.filter(
            Q(titulo__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(tipo_ropa__icontains=query) |
            Q(talla__icontains=query) |
            Q(temporada__icontains=query) |
            Q(usuario__username__icontains=query)
        )
    
    # Ordenar por fecha de creación (opcional)
    donaciones = donaciones.order_by('-fecha_hora')

    # Paginación
    paginator = Paginator(donaciones, 10)  # Mostrar 10 donaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto para la plantilla
    context = {
        'donaciones': page_obj,
        'TIPO_ROPA_CHOICES': Donacion.TIPO_ROPA_CHOICES,
        'TALLAS': Donacion.TALLAS,
        'TEMPORADAS': Donacion.TEMPORADAS,
        'selected_tipo_ropa': tipo_ropa,
        'selected_talla': talla,
        'selected_temporada': temporada,
        'query': query,
        'form': form,
    }

    return render(request, 'menuuser/pedir.html', context)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash, logout

@login_required(login_url='/')
def mi_perfil(request):
    user = request.user  # Asegúrate de obtener el usuario correctamente

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':  # Actualizar el perfil
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.descripcion = request.POST.get('descripcion', '')
            user.direccion = request.POST.get('direccion', '')
            user.telefono = request.POST.get('telefono', '')
            user.email = request.POST.get('email', '')
            user.facebook = request.POST.get('facebook', '')
            user.instagram = request.POST.get('instagram', '')
            user.linkedin = request.POST.get('linkedin', '')

            # Manejo de la foto de perfil
            if request.POST.get('remove_photo') == "true":  # Si se solicitó eliminar la foto
                user.foto_perfil = 'img/nofoto.jpg'  # Establece la imagen por defecto
            elif request.FILES.get('foto_perfil'):
                user.foto_perfil = request.FILES['foto_perfil']

            user.save()  # Guardar los cambios en el usuario
            return redirect('mi_perfil')  # Redirigir a donde necesites después de guardar

        elif form_type == 'change_password':  # Cambiar la contraseña
            current_password = request.POST.get('password')
            new_password = request.POST.get('newpassword')
            renew_password = request.POST.get('renewpassword')

            if new_password == renew_password:
                # Verificar si la contraseña actual es correcta
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()  # Guardar el nuevo password
                    update_session_auth_hash(request, user)  # Mantener la sesión activa
                    logout(request)  # Deslogear al usuario
                    return redirect('/')  # Redirigir a la página de login
                else:
                    # Aquí puedes agregar un mensaje de error si la contraseña actual es incorrecta
                    pass  # Maneja el error como quieras

    return render(request, 'perfil/mi_perfil.html')


@login_required(login_url='/')
def perfil_usuario(request, username):
    # Obtiene el usuario cuyo perfil se está visualizando
    usuario = get_object_or_404(Usuario, username=username)

    # Obtiene las reseñas del usuario
    reseñas_list = Reseña.objects.filter(usuario=usuario)

    # Manejo de la paginación
    paginator = Paginator(reseñas_list, 5)  # Muestra 5 reseñas por página
    page_number = request.GET.get('page')  # Obtiene el número de página desde la URL
    reseñas = paginator.get_page(page_number)  # Obtiene las reseñas para la página actual

    # Manejo del formulario de reseña
    reseña_form = ReseñaForm(request.POST or None)
    if request.method == 'POST' and 'enviar_reseña' in request.POST:
        if reseña_form.is_valid():
            nueva_reseña = reseña_form.save(commit=False)
            nueva_reseña.id_resena = uuid.uuid4()  # Generar un UUID para id_resena
            nueva_reseña.usuario = usuario  # El usuario de la reseña es el perfil que se está visualizando
            nueva_reseña.remitente = request.user  # El remitente es el usuario que está logueado
            nueva_reseña.save()
            return redirect('perfil_usuario', username=username)  # Redirige para evitar reenvíos

    # Manejo del formulario de reporte
    reporte_form = ReporteUsuarioForm(request.POST or None)
    if request.method == 'POST' and 'enviar_reporte' in request.POST:
        if reporte_form.is_valid():
            nuevo_reporte = reporte_form.save(commit=False)
            nuevo_reporte.id_reporte = uuid.uuid4()
            nuevo_reporte.usuario_reportado = usuario  # El usuario que se está reportando
            nuevo_reporte.usuario_reportante = request.user  # El usuario que realiza el reporte
            nuevo_reporte.id_reporte = uuid.uuid4()
            nuevo_reporte.estado = "pendiente"
            nuevo_reporte.save()
            return redirect('perfil_usuario', username=username)  # Redirige para evitar reenvíos

    return render(request, 'perfil/perfil_usuario.html', {
        'usuario': usuario,
        'reseñas': reseñas,  # Aquí pasamos la lista de reseñas paginadas
        'reseña_form': reseña_form,
        'reporte_form': reporte_form,
    })

from .forms import FiltroFundacionForm
from django.db.models import Q
@login_required(login_url='/')
def fundaciones(request):
    # Instanciar el formulario de filtro con los datos del GET
    form = FiltroFundacionForm(request.GET or None)
    
    # Obtener el valor de 'q' (búsqueda) si está presente en la solicitud, o una cadena vacía si no lo está
    query = request.GET.get('q', '')  # 'q' será una cadena vacía si no se pasa como parámetro

    # Filtrar fundaciones aprobadas
    foundations = Fundacion.objects.filter(aprobada=True)

    # Verificar si el formulario es válido y aplicar filtros
    if form.is_valid():
        comuna_region = form.cleaned_data.get('comuna_region')

        # Filtrar por comuna_region si se selecciona una comuna específica
        if comuna_region and comuna_region != 'TODOS':
            foundations = foundations.filter(comuna_region=comuna_region)

        # Filtrar por consulta de búsqueda (si 'q' no está vacío)
        if query:
            foundations = foundations.filter(
                Q(razon_social__icontains=query) | 
                Q(descripcion__icontains=query) |
                Q(direccion__icontains=query) |
                Q(telefono__icontains=query)
            )

    # Paginación
    paginator = Paginator(foundations, 10)  # 10 fundaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'foundations': page_obj,
        'form': form,  # Pasar el formulario al template
        'query': query,  # Asegurarse de pasar la consulta para mantenerla en el formulario
    }
    return render(request, 'menuuser/fundaciones.html', context)




@login_required(login_url='/')
@superuser_required
def modificar_fundacion(request, rut):
    fundacion = get_object_or_404(Fundacion, rut=rut)
    if request.method == 'POST':
        form = FundacionFormMod(request.POST, request.FILES, instance=fundacion)
        if form.is_valid():
            form.save()
            return redirect('fundaciones')  # Redirige a la vista de fundaciones
        else:
            # Imprimir los errores del formulario
            print(form.errors)  # Esto ayudará a diagnosticar problemas
    else:
        form = FundacionForm(instance=fundacion)

    return render(request, 'modificar/mod_fundacion.html', {'form': form})

##class FundacionDetailView(DetailView):
  #  model = Fundacion
   # template_name = 'fundacion_detail.html'


##filtro de donarhtml
from .forms import FiltroPeticionDonacion
@login_required(login_url='/')
def donar(request):
    # Instanciar el formulario con los datos de la solicitud GET
    form = FiltroPeticionDonacion(request.GET or None)
    query = request.GET.get('q', '')  # Obtener búsqueda del usuario, cadena vacía si no se pasa
    tipo_ropa = request.GET.get('tipo_ropa', 'TODOS')  # Valor predeterminado 'TODOS'

    # Aplicar los filtros
    peticiones = Peticion.objects.filter(estado='activa')
    if query:
        peticiones = peticiones.filter(
            Q(titulo__icontains=query) |
            Q(tipo_ropa__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(usuario__username__icontains=query)
        )
    if tipo_ropa != 'TODOS':  # Filtrar por tipo de ropa si está seleccionado
        peticiones = peticiones.filter(tipo_ropa=tipo_ropa)

    # Paginación
    paginator = Paginator(peticiones, 10)  # 10 peticiones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'menuuser/donar.html', {
        'peticiones': page_obj,
        'query': query,
        'form': form
    })

#VISTAS MAPA
@login_required(login_url='/')
def mapa(request):
    query = request.GET.get('q')  # Obtener la búsqueda del usuario
    foundations = Fundacion.objects.filter(aprobada=True)

    return render(request, 'menuuser/mapa.html', {'foundations': foundations})




#CHAT

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversacion
import pytz

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

        # Marcar los mensajes como leídos
        mensajes_no_leidos = mensajes.filter(leido=False)  # Solo los mensajes no leídos
        mensajes_no_leidos.update(leido=True)  # Cambiar el estado de 'leido' a True

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





from django.shortcuts import render, redirect
from .forms import FundacionForm
import uuid

def crear_fundacion(request):
    if request.method == 'POST':
        form = FundacionForm(request.POST, request.FILES)
        if form.is_valid():
            # No guardar aún
            fundacion = form.save(commit=False)
            # Asignar el usuario actual
            fundacion.usuario = request.user
            # Asignar cualquier otro campo necesario
            fundacion.aprobada = False  # Ejemplo, si es necesario
            fundacion.save()  # Guardar la instancia
            return redirect('fundaciones')  # Redirigir a la lista de fundaciones (cambia según tu URL)
    else:
        form = FundacionForm()

    return render(request, 'forms/form_fundacion.html', {'form': form})



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
            donacion.estado = 'activa'  # Establecer estado como 'disponible'
            donacion.donador = request.user  # Asignar el usuario actual como donador
            donacion.usuario = request.user  # Asignar el usuario actual (si este es el campo que necesitas)
            donacion.save()  # Guardar la instancia
            return redirect('pedir')  # Cambia según tu URL
    else:
        form = DonacionForm()

    return render(request, 'forms/form_donacion.html', {'form': form})




@login_required(login_url='/')
@superuser_required
def modificar_peticion(request, id):
    peticion = get_object_or_404(Peticion, id=id)
    if request.method == 'POST':
        form = PeticionFormMod(request.POST, request.FILES, instance=peticion)
        if form.is_valid():
            form.save()
            return redirect('donar')  # Redirige a la vista de fundaciones
        else:
            # Imprimir los errores del formulario
            print(form.errors)  # Esto ayudará a diagnosticar problemas
    else:
        form = PeticionFormMod(instance=peticion)
    usuarios = Usuario.objects.all() 
    return render(request, 'modificar/mod_peticion.html', {'form': form, 'usuarios': usuarios,} )

@login_required(login_url='/')
@superuser_required
def modificar_donacion(request, id):
    donacion = get_object_or_404(Donacion, id=id)
    if request.method == 'POST':
        form = DonacionFormMod(request.POST, request.FILES, instance=donacion)
        if form.is_valid():
            form.save()
            return redirect('pedir')  # Redirige a la vista de fundaciones
        else:
            # Imprimir los errores del formulario
            print(form.errors)  # Esto ayudará a diagnosticar problemas
    else:
        form = DonacionFormMod(instance=donacion)
    usuarios = Usuario.objects.all() 
    return render(request, 'modificar/mod_donacion.html', {'form': form, 'usuarios': usuarios,} )





#ELIMINAR

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Fundacion, Donacion, Peticion

# Vista para eliminar una fundación
@login_required(login_url='/')
@superuser_required
def eliminar_fundacion(request, rut):
    fundacion = get_object_or_404(Fundacion, rut=rut)
    
    fundacion.delete()
    return redirect('fundaciones')  # Cambia esto según tu URL


# Vista para eliminar una donación
@login_required(login_url='/')
@superuser_required
def eliminar_donacion(request, id):
    donacion = get_object_or_404(Donacion, id=id)
    donacion.delete()
    return redirect('donar')  # Cambia esto según tu URL

# Vista para eliminar una petición
@login_required(login_url='/')
@superuser_required
def eliminar_peticion(request, id):
    peticion = get_object_or_404(Peticion, id=id)
    peticion.delete()
    return redirect('pedir')  # Cambia esto según tu URL








#vista admin
@login_required(login_url='/')
@superuser_required
def solicitud_fundaciones(request):
    # Instanciar el formulario de filtro con los datos del GET
    form = FiltroFundacionForm(request.GET or None)
    
    # Obtener el valor de 'q' (búsqueda) si está presente en la solicitud, o una cadena vacía si no lo está
    query = request.GET.get('q', '')  # 'q' será una cadena vacía si no se pasa como parámetro

    # Filtrar fundaciones que tienen el campo 'aprobada' en False
    foundations = Fundacion.objects.filter(aprobada=False)

    # Verificar si el formulario de filtro es válido y aplicar filtros
    if form.is_valid():
        comuna_region = form.cleaned_data.get('comuna_region')

        # Filtrar por comuna_region si se selecciona una comuna específica
        if comuna_region and comuna_region != 'TODOS':
            foundations = foundations.filter(comuna_region=comuna_region)

        # Filtrar por consulta de búsqueda (si 'q' no está vacío)
        if query:
            foundations = foundations.filter(
                Q(razon_social__icontains=query) | 
                Q(descripcion__icontains=query) |
                Q(comuna_region__icontains=query) |  # Cambiado a 'comuna_region'
                Q(direccion__icontains=query) |
                Q(telefono__icontains=query)
            )

    # Paginación
    paginator = Paginator(foundations, 10)  # 10 fundaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pasar los datos al contexto para renderizar la vista
    context = {
        'foundations': page_obj,  # Fundaciones paginadas
        'form': form,  # Pasar el formulario de filtro al template
        'query': query,  # Pasar la consulta de búsqueda para mantenerla en el formulario
    }

    return render(request, 'admin/solicitud_fundaciones.html', context)




@login_required(login_url='/')
@superuser_required
def aprobar_fundacion(request, rut):
    fundacion = get_object_or_404(Fundacion, rut=rut)
    fundacion.aprobada = True
    fundacion.save()
    return redirect('solicitud_fundaciones')  # Redirigir a la vista que muestra las fundaciones




from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ReporteUsuario
import json


from django.shortcuts import render
from .models import ReporteUsuario

def gestionar_reportes(request):
    # Obtener los valores de filtro desde los parámetros GET
    motivo = request.GET.get('motivo', 'TODOS')
    estado = request.GET.get('estado', '')

    # Obtener todos los reportes y aplicar filtros si corresponden
    reportes = ReporteUsuario.objects.all()
    if motivo != 'TODOS':
        reportes = reportes.filter(motivo=motivo)
    if estado:
        reportes = reportes.filter(estado=estado)

    context = {
        'reportes': reportes,
        'MOTIVOS_REPORTE': ReporteUsuario.MOTIVOS_REPORTE,
        'ESTADOS_REPORTE': ReporteUsuario.ESTADOS_REPORTE,
        'selected_motivo': motivo,
        'selected_estado': estado,
    }
    return render(request, 'admin/reportes.html', context)


import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json

logger = logging.getLogger(__name__)

def actualizar_estado_reporte(request, reporte_id, nuevo_estado):
    if request.method == 'POST':
        try:
            # Obtiene el reporte
            reporte = get_object_or_404(ReporteUsuario, id_reporte=reporte_id)
            data = json.loads(request.body)

            # Obtiene el resultado del JSON
            resultado = data.get('resultado', '')

            # Actualiza el estado y resultado del reporte
            reporte.estado = nuevo_estado
            reporte.resultado = resultado
            reporte.save()

            # Enviar correo al usuario reportante
            subject_customer = 'Reporte de Usuario | Upcycle Wear'
            html_content_customer = render_to_string('emails/reporte_estado.html', {'reporte': reporte})
            text_content_customer = strip_tags(html_content_customer)

            email_customer = EmailMultiAlternatives(
                subject=subject_customer,
                body=text_content_customer,
                from_email='upcyclewearcl@gmail.com',  # Cambia esto por tu correo real
                to=[reporte.usuario_reportante.email],
            )
            email_customer.attach_alternative(html_content_customer, "text/html")

            # Envía el correo
            email_customer.send()

            return JsonResponse({'status': 'success'})
        except BadHeaderError:
            logger.error('Bad header error: Invalid header')
            return JsonResponse({'status': 'error', 'message': 'Encabezado de correo no válido'}, status=400)
        except Exception as e:
            logger.error(f'Error inesperado: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método de solicitud no válido'}, status=405)



def actualizar_estado_revisado(request, reporte_id):

    # Obtener el reporte usando el ID
    reporte = ReporteUsuario.objects.get(id_reporte=reporte_id)
    reporte.estado = 'REVISADO'  # Cambiamos el estado a 'REVISADO'
    reporte.save()    
    return redirect('reportes')




@login_required(login_url='/')
def misPeticiones(request, username):
    # Obtener el usuario con el username proporcionado
    user = get_object_or_404(Usuario, username=username)

    # Obtener la búsqueda del usuario desde los parámetros de la URL
    query = request.GET.get('q')
    
    # Obtener solo las peticiones de ese usuario
    peticiones = Peticion.objects.filter(usuario=user)

    # Paginación
    paginator = Paginator(peticiones, 10)  # 10 peticiones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si la solicitud es para finalizar una donación
    if request.method == 'POST' and 'finalizar_donacion' in request.POST:
        donacion_id = request.POST.get('donacion_id')
        donacion = get_object_or_404(Donacion, id=donacion_id, usuario=request.user)

        # Cambia el estado de la donación a "En Progreso"
        donacion.estado = 'En Progreso'
        donacion.save()

        receptor_id = request.POST.get('receptor')
        receptor = get_object_or_404(Usuario, id=receptor_id)
        
        # Asigna el receptor seleccionado a la donación
        donacion.receptor = receptor
        donacion.save()
        
        # Notifica al receptor
        messages.success(request, f"Notificación enviada al receptor {receptor.username}")

        # Redirige a la página de mis peticiones después de finalizar la donación
        return redirect('misPeticiones', username=request.user.username)

    return render(request, 'perfil/mispeticiones.html', {
        'peticiones': page_obj,
        'query': query,
        'username': username  # Pasar el username al contexto para mostrarlo en la plantilla si es necesario
    })



@login_required(login_url='/')
def misDonaciones(request, username):
    user = get_object_or_404(Usuario, username=username)

    # Obtener todas las donaciones del usuario actual y ordenar por fecha, de más reciente a más antiguo
    donaciones = Donacion.objects.filter(usuario=user).order_by('-fecha_hora')  # Asegúrate de que 'fecha' sea el campo correcto

    # Paginación
    paginator = Paginator(donaciones, 10)  # Mostrar 10 donaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con las donaciones
    return render(request, 'perfil/misdonaciones.html', {
        'donaciones': page_obj,
    })



@csrf_exempt
def finalizar_donacion(request, id):
    if request.method == 'POST':
        # Obtener los datos enviados
        data = json.loads(request.body)
        donador_nombre = data.get('donador')
        
        try:
            # Obtener la petición
            peticion = Peticion.objects.get(id=id)
            
            # Obtener el usuario donador
            donador = Usuario.objects.get(username=donador_nombre)  # Primero obtenemos la instancia del Usuario
            
            # Agregar el donador a la petición
            peticion.donador = donador  # Ahora asignamos la instancia del Usuario
            peticion.estado = 'en_proceso'
            peticion.save()
            notificacion_id = uuid.uuid4()
            # Crear una notificación para el donador
            Notificacion.objects.create(
                id=notificacion_id,
                usuario=donador,  # Usamos la instancia del donador
                mensaje=f"El usuario {peticion.usuario.username} ha solicitado finalizar la petición: {peticion.titulo}.",
                leida = False,
                respuesta="PENDIENTE",
                idid = peticion.id,
                tipo = "PETICION"
            )  
            
            return JsonResponse({'success': True})
            
        except Peticion.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Petición no encontrada'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Donador no encontrado'})
        


def aceptar_notificacion(request, notificacion_id):
    # Obtener la notificación
    notificacion = Notificacion.objects.get(id=notificacion_id)
    notificacion.respuesta = 'SI'
    notificacion.leida = True
    notificacion.save()

    # Verificar el tipo de notificación y actualizar el estado en consecuencia
    if notificacion.tipo == "DONACION":
        # Si es de tipo DONACION, actualiza el estado de la donación
        donacion = Donacion.objects.get(id=notificacion.idid)
        donacion.estado = 'completada'
        donacion.save()

        # Incrementar el total de donaciones del usuario donador
        usuario = donacion.usuario
        usuario.total_donaciones += 1
        usuario.save()

    elif notificacion.tipo == "PETICION":
        # Si es de tipo PETICION, actualiza el estado de la petición
        peticion = Peticion.objects.get(id=notificacion.idid)
        peticion.estado = 'completada'
        peticion.save()

        # Incrementar el total de donaciones del usuario que realizó la petición
        usuario = peticion.donador
        usuario.total_donaciones += 1
        usuario.save()

    # Redirigir al origen o a la página de inicio
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def rechazar_notificacion(request, notificacion_id):
    # Obtener la notificación
    notificacion = Notificacion.objects.get(id=notificacion_id)
    notificacion.respuesta = 'NO'
    notificacion.leida = True
    notificacion.save()

    # Verificar el tipo de notificación y actualizar el estado en consecuencia
    if notificacion.tipo == "DONACION":
        # Si es de tipo DONACION, restablece el estado de la donación
        donacion = Donacion.objects.get(id=notificacion.idid)
        donacion.estado = 'activa'
        donacion.save()

    elif notificacion.tipo == "PETICION":
        # Si es de tipo PETICION, restablece el estado de la petición
        peticion = Peticion.objects.get(id=notificacion.idid)
        peticion.estado = 'activa'
        peticion.donador = None  # Elimina el donador asociado
        peticion.save()

    # Redirigir al origen o a la página de inicio
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def notificaciones(request):
    # Obtener todas las notificaciones leídas y no leídas
    notificaciones_leidas = Notificacion.objects.filter(leida=True)
    notificaciones_no_leidas = Notificacion.objects.filter(leida=False)
    
    # Paginación para las notificaciones leídas
    paginator_leidas = Paginator(notificaciones_leidas, 1)  # Mostrar 10 notificaciones por página
    page_leidas = request.GET.get('page')
    notificaciones_leidas_paginas = paginator_leidas.get_page(page_leidas)

    # Paginación para las notificaciones no leídas
    paginator_no_leidas = Paginator(notificaciones_no_leidas, 10)  # Mostrar 10 notificaciones por página
    page_no_leidas = request.GET.get('page')
    notificaciones_no_leidas_paginas = paginator_no_leidas.get_page(page_no_leidas)

    context = {
        'notificaciones_leidas': notificaciones_leidas_paginas,
        'notificaciones_no_leidas': notificaciones_no_leidas_paginas,
    }
    
    return render(request, 'perfil/notificaciones.html', context)

def marcar_como_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    notificacion.marcar_como_leida()
    return redirect('notificaciones') 

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import uuid
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def finalizar_donacion2(request, id):
    if request.method == 'POST':
        # Obtener los datos enviados
        data = json.loads(request.body)
        receptor_nombre = data.get('receptor')  # Cambié 'donador' a 'receptor'
        
        # Verificar si se ha proporcionado el nombre del receptor
        if not receptor_nombre:
            return JsonResponse({'success': False, 'error': 'El nombre del receptor es necesario'})
        
        try:
            # Obtener la donación
            donacion = Donacion.objects.get(id=id)
            logger.debug(f"Donación obtenida: {donacion}")
            
            # Obtener el usuario receptor
            receptor = Usuario.objects.get(username=receptor_nombre)  # Ahora usamos 'receptor'
            logger.debug(f"Receptor encontrado: {receptor}")
            
            # Asignar el receptor y actualizar el estado de la donación
            donacion.receptor = receptor
            donacion.estado = 'en_proceso'  # Cambiar el estado de la donación
            donacion.save()
            logger.debug("Donación actualizada y guardada correctamente.")
            
   
            # Crear una notificación para el receptor
            notificacion_id = uuid.uuid4()
            notificacion = Notificacion.objects.create(
                id=notificacion_id,
                usuario=receptor,
                mensaje=f"El usuario {donacion.usuario.username} ha solicitado finalizar la donación: {donacion.titulo}.",
                leida=False,
                respuesta="PENDIENTE",
                idid=donacion.id,
                tipo="DONACION"
            )
            logger.debug(f"Notificación creada: {notificacion}")

            return JsonResponse({'success': True})
            
        except Donacion.DoesNotExist:
            logger.error("Donación no encontrada.")
            return JsonResponse({'success': False, 'error': 'Donación no encontrada'})
        except Usuario.DoesNotExist:
            logger.error("Receptor no encontrado.")
            return JsonResponse({'success': False, 'error': 'Receptor no encontrado'})
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return JsonResponse({'success': False, 'error': f"Error inesperado: {str(e)}"})

from django.conf import settings

def obtener_mensajes_no_leidos(request):
    if request.user.is_authenticated:
        # Filtrar los mensajes donde el usuario está involucrado como receptor (usuario1 o usuario2),
        # y el mensaje no ha sido leído
        mensajes_no_leidos = Mensaje.objects.filter(
            leido=False
        ).filter(
            # El usuario actual debe ser uno de los participantes (usuario1 o usuario2)
            conversacion__usuario1=request.user
        ).exclude(
            # Asegurarse de que el emisor no sea el usuario actual
            emisor=request.user
        ) | Mensaje.objects.filter(
            leido=False
        ).filter(
            conversacion__usuario2=request.user
        ).exclude(
            emisor=request.user
        )

        # Contar los mensajes no leídos
        contador_mensajes_no_leidos = mensajes_no_leidos.count()

        # Obtener detalles de los mensajes, incluyendo la foto de perfil del emisor
        mensajes_detalles = mensajes_no_leidos[:3].values(
            'id_mensaje', 
            'mensaje', 
            'emisor__username', 
            'fecha_hora', 
            'emisor__foto_perfil',
            'conversacion__id_conversacion' # Asegúrate de incluir la foto de perfil
        )

        # Convertir la URL de la foto a la ruta completa
        for mensaje in mensajes_detalles:
            if mensaje['emisor__foto_perfil']:
                mensaje['emisor__foto_perfil'] = settings.MEDIA_URL + mensaje['emisor__foto_perfil']

        return JsonResponse({
            'contador_mensajes_no_leidos': contador_mensajes_no_leidos,
            'mensajes': list(mensajes_detalles)
        })
    
    return JsonResponse({'contador_mensajes_no_leidos': 0, 'mensajes': []})



from django.views.decorators.http import require_GET
@require_GET
def buscar_usuarios(request):
    query = request.GET.get('q', '')
    usuarios = Usuario.objects.filter(username__icontains=query)[:10]  # Limita a 10 resultados
    resultados = [{'username': user.username,
                    'foto_url': user.foto_perfil.url} for user in usuarios]  # Solo se incluye 'username'
    return JsonResponse(resultados, safe=False)



def cancelar_peticion(request, id):
    # Obtener la petición por su ID o devolver un error si no se encuentra
    peticion = get_object_or_404(Peticion, id=id)
    
    # Cambiar el estado de la petición a "cancelada" o algún estado similar
    peticion.estado = 'cancelada'  # Asumiendo que 'estado' es un campo en el modelo Peticion
    peticion.save()  # Guardar los cambios en la base de datos
    
    # Devolver una respuesta JSON indicando que la operación fue exitosa
    return JsonResponse({'success': True, 'message': 'La petición ha sido cancelada exitosamente.'})

def cancelar_donacion(request, id):
    # Obtener la donación por su ID o devolver un error 404 si no existe
    donacion = get_object_or_404(Donacion, id=id)
    
    # Cambiar el estado de la donación a 'cancelada' o cualquier estado que manejes
    donacion.estado = 'cancelada'  # Asumiendo que 'estado' es un campo en el modelo Donacion
    donacion.save()  # Guardar los cambios en la base de datos
    
    # Retornar una respuesta JSON indicando que la operación fue exitosa
    return JsonResponse({'success': True, 'message': 'La donación ha sido cancelada exitosamente.'})