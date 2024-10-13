
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('', views.principal, name='principal'),
    path('register/', views.register, name='registrarse'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/', views.chat, name='chat'),
    path('donar/', views.donar, name='donar'),
    path('fundaciones/', views.fundaciones, name='fundaciones'),
    path('mapa/', views.mapa, name='mapa'),
    path('pedir/', views.pedir, name='pedir'),
    path('mi_perfil/', views.mi_perfil, name='mi_perfil'),
    path('perfil/<str:username>/', views.perfil_usuario, name='perfil_usuario'),

]   

