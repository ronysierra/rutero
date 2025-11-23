from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==============================================================================
# MODELOS DE USUARIO Y PERFIL
# ==============================================================================

class Perfil(models.Model):
    ROLES = (
        ('LIDER', 'Líder de Zona'),
        ('ASESOR', 'Asesor Comercial'),
    )
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='ASESOR')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    zona = models.CharField(max_length=100, blank=True, null=True, help_text="Zona asignada (ej: Caldas)")

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"

# ==============================================================================
# MODELOS DE NEGOCIO (Rutas y Conjuntos)
# ==============================================================================

class Conjunto(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, help_text="Latitud esperada")
    longitud = models.DecimalField(max_digits=10, decimal_places=7, help_text="Longitud esperada")
    ciudad = models.CharField(max_length=100, default='Manizales')
    
    def __str__(self):
        return self.nombre

class Ruta(models.Model):
    ESTADOS = (
        ('PLAN', 'En Planificación'),
        ('ACTIVA', 'En Curso'),
        ('CERRADA', 'Finalizada'),
    )

    nombre = models.CharField(max_length=200, help_text="Ej: Ruta Centro - Lunes")
    fecha_programada = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PLAN')
    
    # Relaciones
    lider = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, related_name='rutas_creadas')
    asesor_asignado = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, related_name='rutas_asignadas')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.fecha_programada})"

class PuntoVisita(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name='puntos')
    conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField(default=1)
    
    hora_inicio_estimada = models.TimeField(null=True, blank=True)
    hora_fin_estimada = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.orden}. {self.conjunto.nombre}"

# ==============================================================================
# MODELOS DE EJECUCIÓN (Visitas y Evidencias)
# ==============================================================================

class Visita(models.Model):
    ESTADOS_VISITA = (
        ('PENDIENTE', 'Pendiente'),
        ('REALIZADA', 'Realizada / Check-in OK'),
        ('NO_REALIZADA', 'No se pudo realizar'),
    )

    punto_visita = models.OneToOneField(PuntoVisita, on_delete=models.CASCADE, related_name='visita_realizada')
    asesor = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    
    fecha_hora_checkin = models.DateTimeField(auto_now_add=True)
    latitud_registro = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    longitud_registro = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    precision_gps = models.FloatField(help_text="Precisión del GPS en metros", null=True)
    
    estado = models.CharField(max_length=20, choices=ESTADOS_VISITA, default='REALIZADA')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Visita a {self.punto_visita.conjunto.nombre}"

class Evidencia(models.Model):
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE, related_name='evidencias')
    archivo_foto = models.ImageField(upload_to='evidencias/%Y/%m/%d/')
    fecha_captura = models.DateTimeField(auto_now_add=True)
    hash_integridad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Foto visita {self.visita.id}"