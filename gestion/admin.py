from django.contrib import admin
from .models import Perfil, Conjunto, Ruta, PuntoVisita, Visita, Evidencia

# Configuraciones para que se vea bonito en el admin
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'zona', 'telefono')
    list_filter = ('rol',)

@admin.register(Conjunto)
class ConjuntoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'ciudad')
    search_fields = ('nombre',)

# Esto permite agregar puntos de visita directamente dentro de la pantalla de Ruta
class PuntoVisitaInline(admin.TabularInline):
    model = PuntoVisita
    extra = 1

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_programada', 'estado', 'lider', 'asesor_asignado')
    list_filter = ('estado', 'fecha_programada')
    inlines = [PuntoVisitaInline] # ¡Magia! Agrega puntos aquí mismo

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('punto_visita', 'asesor', 'estado', 'fecha_hora_checkin')
    list_filter = ('estado',)

@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ('visita', 'fecha_captura')
