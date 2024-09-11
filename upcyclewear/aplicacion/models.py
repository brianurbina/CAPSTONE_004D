# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('usuario', 'Usuario'),
        ('fundacion', 'Fundación'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    # Campos adicionales para Usuario
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fotoperfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    
    # Campos adicionales para Fundación
    rut = models.CharField(max_length=12, blank=True, null=True)
    logotipo = models.ImageField(upload_to='logotipos/', blank=True, null=True)
