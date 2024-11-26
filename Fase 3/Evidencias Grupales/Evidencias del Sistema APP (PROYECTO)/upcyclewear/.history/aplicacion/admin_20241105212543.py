from django.contrib import admin
from .models import (
    Usuario, Donacion, Conversacion, 
    Mensaje, Fundacion, Peticion, Reseña, ReporteUsuario
)

admin.site.register(Usuario)
admin.site.register(Donacion)
admin.site.register(Conversacion)
admin.site.register(Mensaje)
admin.site.register(Fundacion)
admin.site.register(Peticion)
admin.site.register(Reseña)
admin.site.register(ReporteUsuario)