
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('', views.principal, name='principal'),
    path('newfundacion/', views.register_fundacion, name='newfundacion'),
    path('newusuario/', views.register_usuario, name='newusuario'),
    path('login/', views.user_login, name='user_login'),
    path('index/', views.index, name='index'),
]   

