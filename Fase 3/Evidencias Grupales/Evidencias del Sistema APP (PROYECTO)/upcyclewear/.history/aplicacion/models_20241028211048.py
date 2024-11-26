from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class Usuario(AbstractUser):
       # Tus campos personalizados
       direccion = models.CharField(max_length=255)
       telefono = models.CharField(max_length=20)
       foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True, default='img/nofoto.jpg')
       descripcion = models.TextField(blank=True)

       def __str__(self):
           return self.username
   

class Donacion(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_proceso', 'En proceso'),
        ('donado', 'Donado'),
    ]
    
    id = models.CharField(primary_key=True, max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='donaciones')
    titulo = models.CharField(max_length=100)
    tipo_ropa = models.CharField(max_length=50)
    talla = models.CharField(max_length=20)
    temporada = models.CharField(max_length=20)  # Añadido tipo de campo
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='donaciones/')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    receptor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='donaciones_recibidas')

class HistorialDonaciones(models.Model):
    donacion = models.ForeignKey(Donacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Conversacion(models.Model):
    id_conversacion = models.CharField(primary_key=True, max_length=50)
    usuario1 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='conversaciones_iniciadas')
    usuario2 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='conversaciones_recibidas')

    class Meta:
        unique_together = ('usuario1', 'usuario2')

class Mensaje(models.Model):
    id_mensaje = models.CharField(primary_key=True, max_length=50)
    mensaje = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')


class Reporte(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('revisado', 'Revisado'),
        ('resuelto', 'Resuelto'),
    ]
    
    id = models.CharField(primary_key=True, max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

class Fundacion(models.Model):
    rut = models.CharField(primary_key=True, max_length=20)
    razon_social = models.CharField(max_length=100)
    comuna = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=20)
    logotipo = models.ImageField(upload_to='fundaciones/', null=True, blank=True)
    sitio_web = models.URLField(blank=True)
    aprobada = models.BooleanField(default=False)

class Peticion(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
    ]
    
    id = models.CharField(primary_key=True, max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='peticiones')
    titulo = models.CharField(max_length=100)
    tipo_ropa = models.CharField(max_length=50)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    donador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='donaciones_realizadas')

class HistorialPeticiones(models.Model):
    peticion = models.ForeignKey(Peticion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)



from django.core.validators import MinValueValidator, MaxValueValidator

class Reseña(models.Model):
    id_resena = models.UUIDField(primary_key=True)  # ID generado automáticamente por el modelo
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    estrellas = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    reseña = models.CharField(max_length=255, default='Sin comentarios')

    def __str__(self):
        return str(self.id_resena)  # Cambiar a id_resena
