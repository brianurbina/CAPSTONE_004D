from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class Usuario(AbstractUser):
       # Tus campos personalizados
       direccion = models.CharField(max_length=255)
       telefono = models.CharField(max_length=20)
       foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True, default='img/nofoto.jpg')
       descripcion = models.TextField(blank=True)
       facebook= models.URLField( default= "https://www.facebook.com/")
       instagram= models.URLField(default= "https://www.instagram.com/")
       linkedin= models.URLField( default= "https://www.linkedin.com/")

       def __str__(self):
           return self.username




class Donacion(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    TIPO_ROPA_CHOICES = [
    ('', 'Seleccione una opción'),  # Opción por defecto
    # Ropa Superior
    ('Ropa Superior', [
        ('camiseta', 'Camiseta'),
        ('polo', 'Polo'),
        ('blusa', 'Blusa'),
        ('camisa', 'Camisa'),
        ('top', 'Top'),
        ('sueter', 'Suéter'),
        ('sudadera', 'Sudadera'),
        ('chaqueta', 'Chaqueta'),
        ('abrigo', 'Abrigo'),
        ('cardigan', 'Cárdigan'),
        ('chaleco', 'Chaleco'),
        ('camiseta_sin_mangas', 'Camiseta sin mangas'),
        ('blazer', 'Saco o Blazer'),
        ('jersey', 'Jersey'),
    ]),
    # Ropa Inferior
    ('Ropa Inferior', [
        ('pantalon', 'Pantalón'),
        ('falda', 'Falda'),
        ('shorts', 'Shorts'),
        ('bermudas', 'Bermudas'),
        ('leggings', 'Leggings'),
        ('capris', 'Capris'),
    ]),
    # Vestidos
    ('Vestidos', [
        ('vestido_fiesta', 'Vestido de Fiesta'),
        ('vestido_casual', 'Vestido Casual'),
        ('vestido_noche', 'Vestido de Noche'),
        ('vestido_largo', 'Vestido Largo'),
        ('vestido_corto', 'Vestido Corto'),
        ('vestido_coctel', 'Vestido de Cóctel'),
        ('maxi_vestido', 'Maxi Vestido'),
    ]),
    # Ropa Íntima
    ('Ropa Íntima', [
        ('sujetador', 'Sujetador'),
        ('calzoncillos', 'Calzoncillos'),
        ('bragas', 'Bragas'),
        ('bodysuit', 'Bodysuit'),
        ('camiseta_interior', 'Camiseta interior'),
        ('faja', 'Faja'),
        ('corset', 'Corset'),
        ('camison', 'Camisón'),
        ('pijama', 'Pijamas'),
        ('batas_dormir', 'Batas de dormir'),
    ]),
    # Ropa de Exterior
    ('Ropa de Exterior', [
        ('abrigo', 'Abrigo'),
        ('chaqueta', 'Chaqueta'),
        ('gabardina', 'Gabardina o Trench'),
        ('parka', 'Parka'),
        ('poncho', 'Poncho'),
        ('capa', 'Capa'),
        ('impermeable', 'Impermeable'),
        ('chaleco_acolchado', 'Chaleco acolchado'),
    ]),
    # Ropa Deportiva
    ('Ropa Deportiva', [
        ('sudadera', 'Sudadera'),
        ('pantalon_deportivo', 'Pantalón deportivo'),
        ('shorts_deportivos', 'Shorts deportivos'),
        ('leggings_deportivos', 'Leggings deportivos'),
        ('top_deportivo', 'Top deportivo'),
        ('traje_bano', 'Traje de baño'),
        ('bikini', 'Bikini'),
        ('ropa_ciclismo', 'Ropa de ciclismo'),
        ('ropa_yoga', 'Ropa de yoga'),
    ]),
    # Ropa de Bebé
    ('Ropa de Bebé', [
        ('body', 'Body'),
        ('pelele', 'Pelele'),
        ('mameluco', 'Mameluco'),
        ('babero', 'Babero'),
        ('pantalones_bebe', 'Pantalones para bebé'),
        ('conjuntos_bebe', 'Conjuntos'),
        ('polainas', 'Polainas'),
        ('pijamas_bebe', 'Pijamas para bebé'),
        ('chaleco_acolchado_bebe', 'Chaleco acolchado para bebé'),
    ]),
    # Trajes
    ('Trajes', [
        ('traje_dos_piezas', 'Traje de dos piezas'),
        ('esmoquin', 'Esmoquin'),
        ('traje_tres_piezas', 'Traje de tres piezas'),
        ('conjunto_falda', 'Conjunto de falda y chaqueta'),
        ('conjunto_pantalon', 'Conjunto de pantalón y top'),
    ]),
    # Accesorios de Ropa
    ('Accesorios de Ropa', [
        ('bufanda', 'Bufanda'),
        ('guantes', 'Guantes'),
        ('sombrero', 'Sombrero'),
        ('cinturon', 'Cinturón'),
        ('panuelo', 'Pañuelo'),
        ('calcetines', 'Calcetines'),
        ('ligas', 'Ligas'),
        ('chal', 'Chal'),
    ]),
    # Uniformes
    ('Uniformes', [
        ('uniforme_escolar', 'Uniforme escolar'),
        ('uniforme_trabajo', 'Uniforme de trabajo'),
        ('ropa_enfermeria', 'Ropa de enfermería'),
        ('uniforme_deportivo', 'Uniforme deportivo'),
        ('traje_proteccion', 'Traje de protección'),
        ('uniforme_militar', 'Uniforme militar'),
    ]),
    # Trajes Tradicionales
    ('Trajes Tradicionales', [
        ('kimono', 'Kimono'),
        ('sari', 'Sari'),
        ('traje_folclorico', 'Traje folclórico'),
        ('traje_flamenco', 'Traje de flamenco'),
        ('traje_charro', 'Traje charro'),
        ('toga', 'Toga'),
    ]),
    # Ropa Especializada
    ('Ropa Especializada', [
        ('ropa_maternidad', 'Ropa de maternidad'),
        ('ropa_seguridad', 'Ropa de seguridad'),
        ('ropa_lluvia', 'Ropa de lluvia'),
        ('traje_nieve', 'Traje de nieve'),
        ('traje_neopreno', 'Traje de neopreno'),
    ]),
]
    TALLAS = [
    ('0-3m', '0-3 meses'),
    ('3-6m', '3-6 meses'),
    ('6-9m', '6-9 meses'),
    ('9-12m', '9-12 meses'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large'),
]
    TEMPORADAS = [
    ('primavera', 'Primavera'),
    ('verano', 'Verano'),
    ('otono', 'Otoño'),
    ('invierno', 'Invierno'),
]
    id = models.CharField(primary_key=True, max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='donaciones')
    titulo = models.CharField(max_length=100)
    tipo_ropa = models.CharField(max_length=50,choices=TIPO_ROPA_CHOICES)
    talla = models.CharField(max_length=20,choices=TALLAS, default='M',)
    temporada = models.CharField(max_length=20 , choices=TEMPORADAS,default='primavera')  # Añadido tipo de campo
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='donaciones/')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES  ,blank=True,  null=True )
    receptor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True,  null=True, related_name='donaciones_recibidas')


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



class Fundacion(models.Model):
    # Definimos las regiones y sus comunas
    REGIONES_Y_COMUNAS = [
    ('', 'Seleccione una opción'),  # Opción por defecto
    # Comunas de la Región Metropolitana
    ('Región Metropolitana', [
        ('santiago', 'Santiago'),
        ('maipu', 'Maipú'),
        ('providencia', 'Providencia'),
        ('las_condes', 'Las Condes'),
        ('ñunoa', 'Ñuñoa'),
        ('vitacura', 'Vitacura'),
        ('la_florida', 'La Florida'),
        ('peñalolen', 'Peñalolén'),
        ('el_bosque', 'El Bosque'),
        ('la_reina', 'La Reina'),
        ('pudahuel', 'Pudahuel'),
        ('independencia', 'Independencia'),
        ('san_miguel', 'San Miguel'),
        ('san_joaquin', 'San Joaquín'),
        ('macul', 'Macul'),
    ]),
    # Comunas de la Región de Valparaíso
    ('Región de Valparaíso', [
        ('valparaiso', 'Valparaíso'),
        ('vina_del_mar', 'Viña del Mar'),
        ('quillota', 'Quillota'),
        ('san_antonio', 'San Antonio'),
        ('san_felipe', 'San Felipe'),
        ('villa_alegre', 'Villa Alegre'),
        ('almargen', 'Almargen'),
        ('almendral', 'Almendral'),
        ('cachagua', 'Cachagua'),
        ('zapallar', 'Zapallar'),
    ]),
    # Comunas de la Región de Coquimbo
    ('Región de Coquimbo', [
        ('la_serena', 'La Serena'),
        ('coquimbo', 'Coquimbo'),
        ('combarbala', 'Combarbalá'),
        ('illapel', 'Illapel'),
        ('andacollo', 'Andacollo'),
        ('punitaqui', 'Punitaqui'),
        ('ovalle', 'Ovalle'),
        ('punta_arenas', 'Punta Arenas'),
        ('peñuelas', 'Peñuelas'),
    ]),
    # Comunas de la Región de Antofagasta
    ('Región de Antofagasta', [
        ('antofagasta', 'Antofagasta'),
        ('calama', 'Calama'),
        ('mejillones', 'Mejillones'),
        ('tocopilla', 'Tocopilla'),
        ('sierra_gorda', 'Sierra Gorda'),
        ('maria_elena', 'María Elena'),
    ]),
    # Comunas de la Región de Atacama
    ('Región de Atacama', [
        ('copiapo', 'Copiapó'),
        ('vallenar', 'Vallenar'),
        ('chilecito', 'Chilecito'),
        ('caldera', 'Caldera'),
        ('huasco', 'Huasco'),
        ('freirina', 'Freirina'),
    ]),
    # Comunas de la Región de Araucanía
    ('Región de Araucanía', [
        ('temuco', 'Temuco'),
        ('angol', 'Angol'),
        ('villarrica', 'Villarrica'),
        ('pitrufquen', 'Pitrufquén'),
        ('freire', 'Freire'),
        ('carahue', 'Carahue'),
        ('teodoro_schmidt', 'Teodoro Schmidt'),
        ('lachauco', 'Lachauco'),
    ]),
    # Comunas de la Región de Los Ríos
    ('Región de Los Ríos', [
        ('valdivia', 'Valdivia'),
        ('la_union', 'La Unión'),
        ('rio_negro', 'Río Negro'),
        ('corral', 'Corral'),
        ('los_lagos', 'Los Lagos'),
        ('llanquihue', 'Llanquihue'),
    ]),
    # Comunas de la Región de Los Lagos
    ('Región de Los Lagos', [
        ('osorno', 'Osorno'),
        ('puerto_montt', 'Puerto Montt'),
        ('castro', 'Castro'),
        ('ancud', 'Ancud'),
        ('puyehue', 'Puyehue'),
        ('los_muermos', 'Los Muermos'),
        ('maullín', 'Maullín'),
    ]),
    # Comunas de la Región de Magallanes
    ('Región de Magallanes', [
        ('punta_arenas', 'Punta Arenas'),
        ('porvenir', 'Porvenir'),
        ('cabo_de_hornos', 'Cabo de Hornos'),
        ('primavera', 'Primavera'),
        ('serrano', 'Serrano'),
    ]),
    # Comunas de la Región de Arica y Parinacota
    ('Región de Arica y Parinacota', [
        ('arica', 'Arica'),
        ('putre', 'Putre'),
        ('camarones', 'Camarones'),
    ]),
    # Comunas de la Región de Tarapacá
    ('Región de Tarapacá', [
        ('iquique', 'Iquique'),
        ('alto_hospicio', 'Alto Hospicio'),
        ('pica', 'Pica'),
        ('migración', 'Migración'),
    ]),
    # Comunas de la Región de Antofagasta
    ('Región de Antofagasta', [
        ('antofagasta', 'Antofagasta'),
        ('calama', 'Calama'),
        ('mejillones', 'Mejillones'),
        ('tocopilla', 'Tocopilla'),
        ('sierra_gorda', 'Sierra Gorda'),
    ]),
    # Comunas de la Región de Ñuble
    ('Región de Ñuble', [
        ('chillan', 'Chillán'),
        ('bulnes', 'Bulnes'),
        ('quillan', 'Quillán'),
        ('yungay', 'Yungay'),
    ]),
]


    rut = models.CharField(primary_key=True, max_length=20)
    razon_social = models.CharField(max_length=100)
    comuna_region = models.CharField(max_length=50, choices=REGIONES_Y_COMUNAS, default='')
    direccion = models.CharField(max_length=255)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=20)
    logotipo = models.ImageField(upload_to='fundaciones/', null=True, blank=True, default='img/nofoto.jpg')
    sitio_web = models.URLField(blank=True)
    aprobada = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='dueño')

class Peticion(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    # Definimos las opciones para el campo tipo_ropa
    TIPO_ROPA_CHOICES = [
    ('', 'Seleccione una opción'),  # Opción por defecto
    # Ropa Superior
    ('Ropa Superior', [
        ('camiseta', 'Camiseta'),
        ('polo', 'Polo'),
        ('blusa', 'Blusa'),
        ('camisa', 'Camisa'),
        ('top', 'Top'),
        ('sueter', 'Suéter'),
        ('sudadera', 'Sudadera'),
        ('chaqueta', 'Chaqueta'),
        ('abrigo', 'Abrigo'),
        ('cardigan', 'Cárdigan'),
        ('chaleco', 'Chaleco'),
        ('camiseta_sin_mangas', 'Camiseta sin mangas'),
        ('blazer', 'Saco o Blazer'),
        ('jersey', 'Jersey'),
    ]),
    # Ropa Inferior
    ('Ropa Inferior', [
        ('pantalon', 'Pantalón'),
        ('falda', 'Falda'),
        ('shorts', 'Shorts'),
        ('bermudas', 'Bermudas'),
        ('leggings', 'Leggings'),
        ('capris', 'Capris'),
    ]),
    # Vestidos
    ('Vestidos', [
        ('vestido_fiesta', 'Vestido de Fiesta'),
        ('vestido_casual', 'Vestido Casual'),
        ('vestido_noche', 'Vestido de Noche'),
        ('vestido_largo', 'Vestido Largo'),
        ('vestido_corto', 'Vestido Corto'),
        ('vestido_coctel', 'Vestido de Cóctel'),
        ('maxi_vestido', 'Maxi Vestido'),
    ]),
    # Ropa Íntima
    ('Ropa Íntima', [
        ('sujetador', 'Sujetador'),
        ('calzoncillos', 'Calzoncillos'),
        ('bragas', 'Bragas'),
        ('bodysuit', 'Bodysuit'),
        ('camiseta_interior', 'Camiseta interior'),
        ('faja', 'Faja'),
        ('corset', 'Corset'),
        ('camison', 'Camisón'),
        ('pijama', 'Pijamas'),
        ('batas_dormir', 'Batas de dormir'),
    ]),
    # Ropa de Exterior
    ('Ropa de Exterior', [
        ('abrigo', 'Abrigo'),
        ('chaqueta', 'Chaqueta'),
        ('gabardina', 'Gabardina o Trench'),
        ('parka', 'Parka'),
        ('poncho', 'Poncho'),
        ('capa', 'Capa'),
        ('impermeable', 'Impermeable'),
        ('chaleco_acolchado', 'Chaleco acolchado'),
    ]),
    # Ropa Deportiva
    ('Ropa Deportiva', [
        ('sudadera', 'Sudadera'),
        ('pantalon_deportivo', 'Pantalón deportivo'),
        ('shorts_deportivos', 'Shorts deportivos'),
        ('leggings_deportivos', 'Leggings deportivos'),
        ('top_deportivo', 'Top deportivo'),
        ('traje_bano', 'Traje de baño'),
        ('bikini', 'Bikini'),
        ('ropa_ciclismo', 'Ropa de ciclismo'),
        ('ropa_yoga', 'Ropa de yoga'),
    ]),
    # Ropa de Bebé
    ('Ropa de Bebé', [
        ('body', 'Body'),
        ('pelele', 'Pelele'),
        ('mameluco', 'Mameluco'),
        ('babero', 'Babero'),
        ('pantalones_bebe', 'Pantalones para bebé'),
        ('conjuntos_bebe', 'Conjuntos'),
        ('polainas', 'Polainas'),
        ('pijamas_bebe', 'Pijamas para bebé'),
        ('chaleco_acolchado_bebe', 'Chaleco acolchado para bebé'),
    ]),
    # Trajes
    ('Trajes', [
        ('traje_dos_piezas', 'Traje de dos piezas'),
        ('esmoquin', 'Esmoquin'),
        ('traje_tres_piezas', 'Traje de tres piezas'),
        ('conjunto_falda', 'Conjunto de falda y chaqueta'),
        ('conjunto_pantalon', 'Conjunto de pantalón y top'),
    ]),
    # Accesorios de Ropa
    ('Accesorios de Ropa', [
        ('bufanda', 'Bufanda'),
        ('guantes', 'Guantes'),
        ('sombrero', 'Sombrero'),
        ('cinturon', 'Cinturón'),
        ('panuelo', 'Pañuelo'),
        ('calcetines', 'Calcetines'),
        ('ligas', 'Ligas'),
        ('chal', 'Chal'),
    ]),
    # Uniformes
    ('Uniformes', [
        ('uniforme_escolar', 'Uniforme escolar'),
        ('uniforme_trabajo', 'Uniforme de trabajo'),
        ('ropa_enfermeria', 'Ropa de enfermería'),
        ('uniforme_deportivo', 'Uniforme deportivo'),
        ('traje_proteccion', 'Traje de protección'),
        ('uniforme_militar', 'Uniforme militar'),
    ]),
    # Trajes Tradicionales
    ('Trajes Tradicionales', [
        ('kimono', 'Kimono'),
        ('sari', 'Sari'),
        ('traje_folclorico', 'Traje folclórico'),
        ('traje_flamenco', 'Traje de flamenco'),
        ('traje_charro', 'Traje charro'),
        ('toga', 'Toga'),
    ]),
    # Ropa Especializada
    ('Ropa Especializada', [
        ('ropa_maternidad', 'Ropa de maternidad'),
        ('ropa_seguridad', 'Ropa de seguridad'),
        ('ropa_lluvia', 'Ropa de lluvia'),
        ('traje_nieve', 'Traje de nieve'),
        ('traje_neopreno', 'Traje de neopreno'),
    ]),
]

    
    id = models.CharField(primary_key=True, max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='peticiones')
    titulo = models.CharField(max_length=100)
    tipo_ropa = models.CharField(max_length=50, choices=TIPO_ROPA_CHOICES, default='')
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    donador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='donaciones_realizadas')


class Reseña(models.Model):
    id_resena = models.UUIDField(primary_key=True)  # ID generado automáticamente por el modelo
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,  related_name='dueñoperfil')
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE,  related_name='dueñoreseña')
    estrellas = models.IntegerField(
        null=True,
        blank=True,
        default=3,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    reseña = models.CharField(max_length=255,blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id_resena)  # Cambiar a id_resena



class ReporteUsuario(models.Model):
    MOTIVOS_REPORTE = [
        ('SPAM', 'Spam'),
        ('ACOSO', 'Acoso'),
        ('CONTENIDO_INAPROPIADO', 'Contenido Inapropiado'),
        ('OTRO', 'Otro'),
    ]

    ESTADOS_REPORTE = [
        ('PENDIENTE', 'Pendiente'),
        ('REVISADO', 'Revisado'),
        ('RESUELTO', 'Resuelto'),
        ('RECHAZADO', 'Rechazado'),
    ]
    id_reporte = models.CharField(primary_key=True, max_length=50)
    usuario_reportado = models.ForeignKey(Usuario, related_name='reportes_recibidos', on_delete=models.CASCADE)
    usuario_reportante = models.ForeignKey(Usuario, related_name='reportes_realizados', on_delete=models.CASCADE)
    motivo = models.CharField(max_length=50, choices=MOTIVOS_REPORTE)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_REPORTE, default='PENDIENTE')
    resultado= models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Reporte de Usuario'
        verbose_name_plural = 'Reportes de Usuarios'

    def __str__(self):
        return f'Reporte de {self.usuario_reportante} sobre {self.usuario_reportado} - {self.get_motivo_display()}'

"""
class Region(models.Model):
    id= models.CharField(primary_key=True, max_length=50)
    region = models.CharField(max_length=50)

    def __str__(self):
        return f'id: {self.id} region: {self.region}'

class Comuna(models.Model):
    id= models.CharField(primary_key=True, max_length=50)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='region')
    comuna = models.CharField(max_length=50)
    def __str__(self):
        return f'id: {self.id} region: {self.comuna}'
"""

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)  # Para saber si el usuario vio la notificación

    def __str__(self):
        return f"Notificación para {self.usuario.username} - {self.mensaje}"

    def marcar_como_leida(self):
        self.leida = True
        self.save()