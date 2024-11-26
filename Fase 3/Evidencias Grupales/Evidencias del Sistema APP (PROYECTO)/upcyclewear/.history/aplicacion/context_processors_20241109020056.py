from .models import Notificacion

def notificaciones(request):
    if request.user.is_authenticated:
        # Obtener las notificaciones no leídas para el usuario autenticado
        notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
        return {'notificaciones': notificaciones}
    return {'notificaciones': []}

from django.http import JsonResponse
from .models import Mensaje

def obtener_mensajes_no_leidos(request):
    if request.user.is_authenticated:
        # Obtener los mensajes no leídos para el usuario autenticado
        mensajes_no_leidos = Mensaje.objects.filter(conversacion__usuario=request.user, leido=False)

        # Contar los mensajes no leídos
        contador_mensajes_no_leidos = mensajes_no_leidos.count()

        # Obtener detalles de los mensajes (por ejemplo, los 3 más recientes)
        mensajes_detalles = mensajes_no_leidos[:3].values('id_mensaje', 'mensaje', 'emisor__username', 'fecha_hora')

        return JsonResponse({
            'contador_mensajes_no_leidos': contador_mensajes_no_leidos,
            'mensajes': list(mensajes_detalles)
        })
    return JsonResponse({'contador_mensajes_no_leidos': 0, 'mensajes': []})
