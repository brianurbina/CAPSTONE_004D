
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('', views.principal, name='principal'),
    path('register/', views.register, name='registrarse'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
  
]   

