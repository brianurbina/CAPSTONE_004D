from django.contrib import admin
from .models import (
    Usuario, Donacion, HistorialDonaciones, Conversacion, 
    Mensaje, Reporte, Fundacion, Peticion, HistorialPeticiones
)

admin.site.register(Usuario)
admin.site.register(Donacion)
admin.site.register(HistorialDonaciones)
admin.site.register(Conversacion)
admin.site.register(Mensaje)
admin.site.register(Reporte)
admin.site.register(Fundacion)
admin.site.register(Peticion)
admin.site.register(HistorialPeticiones)
