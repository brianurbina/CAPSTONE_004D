from .models import Notificacion

def notificaciones(request):
    if request.user.is_authenticated:
        # Obtener las notificaciones no leídas para el usuario autenticado
        notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
        return {'notificaciones': notificaciones}
    return {'notificaciones': []}

from .models import Mensaje

def mensajes_no_leidos(request):
    if request.user.is_authenticated:
        # Obtener los mensajes no leídos para el usuario autenticado
        mensajes_no_leidos = Mensaje.objects.filter(conversacion__usuario=request.user, leido=False)
        
        # Contar los mensajes no leídos
        contador_mensajes_no_leidos = mensajes_no_leidos.count()
        
        # Pasar los mensajes no leídos y el contador al template
        return {'mensajes_no_leidos': mensajes_no_leidos, 'contador_mensajes_no_leidos': contador_mensajes_no_leidos}
    
    return {'mensajes_no_leidos': [], 'contador_mensajes_no_leidos': 0}
