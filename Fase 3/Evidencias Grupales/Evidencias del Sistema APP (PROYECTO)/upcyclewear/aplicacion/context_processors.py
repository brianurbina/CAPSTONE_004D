from .models import Notificacion

def notificaciones(request):
    if request.user.is_authenticated:
        # Obtener las notificaciones no leídas para el usuario autenticado
        notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
        return {'notificaciones': notificaciones}
    return {'notificaciones': []}

