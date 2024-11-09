from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioRegisterForm, FundacionForm, PeticionForm, DonacionForm, FundacionFormMod, ReseñaForm, ReporteUsuarioForm, PeticionFormMod, DonacionFormMod
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Usuario, Fundacion, Peticion, Donacion, Conversacion, Mensaje, Reseña, ReporteUsuario
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


@login_required(login_url='/')
def pedir(request):
    query = request.GET.get('q')  # Obtener la búsqueda del usuario

    if query:
        donaciones = Donacion.objects.filter(
            Q(titulo__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(tipo_ropa__icontains=query) |
            Q(talla__icontains=query) |
            Q(temporada__icontains=query) |
            Q(usuario__username__icontains=query)
        )
    else:
        # Obtener todas las donaciones del usuario actual
        donaciones = Donacion.objects.all().order_by('-fecha_hora')  # Ordenar por fecha, de más reciente a más antiguo

    # Paginación (opcional)
    paginator = Paginator(donaciones, 10)  # Mostrar 3 donaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con las donaciones
    return render(request, 'menuuser/pedir.html', {
        'donaciones': page_obj,
        'query': query
    })


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
    # Instanciar el formulario de filtro con los datos del GET
    form = FiltroFundacionForm(request.GET or None)
    
    # Obtener el valor de 'q' (búsqueda) si está presente en la solicitud, o una cadena vacía si no lo está
    query = request.GET.get('q', '')  # 'q' será una cadena vacía si no se pasa como parámetro

    # Filtrar fundaciones aprobadas
    foundations = Fundacion.objects.filter(aprobada=True)

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
                Q(direccion__icontains=query) |
                Q(telefono__icontains=query)
            )
    
    # Obtener la fundación a modificar según el 'rut'
    fundacion = get_object_or_404(foundations, rut=rut)

    # Si se hace una petición POST para modificar la fundación
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

    return render(request, 'modificar/mod_fundacion.html', {
        'form': form,
        'foundations': foundations,  # Pasar las fundaciones filtradas al template
        'query': query,  # Pasar la consulta de búsqueda al template
        'form_filter': form,  # Pasar el formulario de filtro al template
    })

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
    paginator = Paginator(peticiones, 10)  # 3 peticiones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'menuuser/donar.html', {
        'peticiones': page_obj,
        'query': query
    })



#VISTAS MAPA
@login_required(login_url='/')
def mapa(request):
    query = request.GET.get('q')  # Obtener la búsqueda del usuario
    if query:
        foundations = Fundacion.objects.filter(
            Q(razon_social__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(comuna_region__icontains=query) |
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
            donacion.estado = 'disponible'  # Establecer estado como 'disponible'
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
        form = FundacionForm(instance=peticion)
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
        form = FundacionForm(instance=donacion)
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
    query = request.GET.get('q')  # Obtener la búsqueda del usuario

    # Filtrar fundaciones que tienen el campo 'aprobada' en False
    foundations = Fundacion.objects.filter(aprobada=False)

    # Si hay una consulta de búsqueda, filtra también por ella
    if query:
        foundations = foundations.filter(
            Q(razon_social__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(comuna__icontains=query) |
            Q(region__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query)
        )

    # Paginación
    paginator = Paginator(foundations, 10)  # 10 fundaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/solicitud_fundaciones.html', {'foundations': page_obj, 'query': query})


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