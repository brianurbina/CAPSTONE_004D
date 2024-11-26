
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('', views.principal, name='principal'),
    path('register/', views.register, name='registrarse'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/', views.ver_conversacion, name='chat'),  # Cambiado aquí
    path('donar/', views.donar, name='donar'),
    path('donar/nuevadonacion/', views.crear_donacion, name='crear_donacion'),
    path('fundaciones/', views.fundaciones, name='fundaciones'),
    path('fundaciones/nueva/', views.crear_fundacion, name='crear_fundacion'),
    path('mapa/', views.mapa, name='mapa'),

    path('pedir/', views.pedir, name='pedir'),
    path('pedir/nuevapeticion/', views.crear_peticion, name='crear_peticion'),
    path('mi_perfil/', views.mi_perfil, name='mi_perfil'),
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),
    path('guardar-mensaje/', views.guardar_mensaje, name='guardar_mensaje'),
    path('crear-conversacion/<str:usuario_username>/', views.crear_conversacion, name='crear_conversacion'),
    path('fundacion/modificar/<str:rut>/', views.modificar_fundacion, name='modificar_fundacion'),
    path('peticion/modificar/<str:id>/', views.modificar_peticion, name='modificar_peticion'),
    path('donacion/modificar/<str:id>/', views.modificar_donacion, name='modificar_donacion'),
    path('eliminar-fundacion/<str:rut>/', views.eliminar_fundacion, name='eliminar_fundacion'),
    path('eliminar-donacion/<str:id>/', views.eliminar_donacion, name='eliminar_donacion'),
    path('eliminar-peticion/<str:id>/', views.eliminar_peticion, name='eliminar_peticion'),
    path('administrador/solicitud_fundaciones/', views.solicitud_fundaciones, name='solicitud_fundaciones'),
    path('aprobar_fundacion/<str:rut>/', views.aprobar_fundacion, name='aprobar_fundacion'),
    path('reportes/', views.gestionar_reportes, name='reportes'),
    path('actualizar_estado_reporte/<uuid:reporte_id>/<str:nuevo_estado>/', views.actualizar_estado_reporte, name='actualizar_estado_reporte'),
    path('actualizar_estado_revisado/<uuid:reporte_id>/', views.actualizar_estado_revisado, name='actualizar_estado_revisado'),
    path('peticiones/<str:username>/', views.misPeticiones, name='misPeticiones'),
    path('donaciones/<str:username>/', views.misDonaciones, name='misDonaciones'),
    path('finalizar_donacion/<uuid:id>/', views.finalizar_donacion, name='finalizar_donacion'),
    path('notificacion/aceptar/<uuid:notificacion_id>/', views.aceptar_notificacion, name='aceptar_notificacion'),
    path('notificacion/rechazar/<uuid:notificacion_id>/', views.rechazar_notificacion, name='rechazar_notificacion'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('notificacion/marcar-como-leida/<uuid:notificacion_id>/', views.marcar_como_leida, name='marcar_como_leida'),
    path('finalizar_donacion2/<uuid:id>/', views.finalizar_donacion2, name='finalizar_donacion2'),
    path('obtener_mensajes_no_leidos/', views.obtener_mensajes_no_leidos, name='obtener_mensajes_no_leidos'),
    path('buscar_usuarios/', views.buscar_usuarios, name='buscar_usuarios'),
    path('cancelar_donacion/<uuid:id>/', views.cancelar_donacion, name='cancelar_donacion'),
    path('cancelar_peticion/<uuid:id>/', views.cancelar_peticion, name='cancelar_peticion'),

]   