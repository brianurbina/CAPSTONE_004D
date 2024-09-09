# mi_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
]
