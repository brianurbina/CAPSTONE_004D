
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
]