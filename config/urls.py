from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views as token_views
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone
# Importamos tus modelos para el script de población
from gestion.models import Perfil, Conjunto, Ruta, PuntoVisita

# ==============================================================================
# 1. CONFIGURACIÓN DE SWAGGER (Documentación)
# ==============================================================================
schema_view = get_schema_view(
   openapi.Info(
      title="API Rutero Verde y Limpio",
      default_version='v1',
      description="Documentación técnica de la API para el seguimiento de asesores.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="soporte@ruteroverde.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# ==============================================================================
# 2. VISTA PARA POBLAR BASE DE DATOS (Backdoor Temporal)
# ==============================================================================
def poblar_db_view(request):
    log = [] 
    try:
        # A. Forzar Migraciones (Crear tablas si no existen)
        call_command('migrate', interactive=False)
        log.append("✅ Tablas verificadas/migradas.")

        # B. Crear Conjuntos
        conjuntos_data = [
            {"nombre": "Torres de Milán", "direccion": "Cra 23 # 55-10", "lat": 1.612, "lng": -75.601},
            {"nombre": "Edificio Los Rosales", "direccion": "Calle 65 # 24-12", "lat": 1.615, "lng": -75.605},
            {"nombre": "Conjunto Cerrado El Bosque", "direccion": "Av Santander # 45-20", "lat": 1.618, "lng": -75.602},
            {"nombre": "Residencial La Colina", "direccion": "Cra 15 # 12-30", "lat": 1.620, "lng": -75.608},
            {"nombre": "Urbanización Los Cámbulos", "direccion": "Calle 10 # 5-50", "lat": 1.622, "lng": -75.610},
        ]

        conjuntos_objs = []
        for c in conjuntos_data:
            obj, created = Conjunto.objects.get_or_create(
                nombre=c["nombre"],
                defaults={
                    "direccion": c["direccion"],
                    "latitud": c["lat"],
                    "longitud": c["lng"],
                    "ciudad": "Manizales"
                }
            )
            conjuntos_objs.append(obj)
        log.append(f"✅ {len(conjuntos_objs)} Conjuntos listos.")

        # C. Crear Usuarios y Perfiles
        usuarios_data = [
            ("admin", "admin1234", "LIDER", "Admin Super"), # Superusuario
            ("lider.demo", "lider123", "LIDER", "Carlos Líder"),
            ("asesor.juan", "asesor123", "ASESOR", "Juan Pérez"),
            ("asesor.maria", "asesor123", "ASESOR", "María González"),
        ]

        perfiles = {}

        for username, password, rol, nombre in usuarios_data:
            # Crear usuario base
            if username == 'admin':
                if not User.objects.filter(username='admin').exists():
                    user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin1234')
                else:
                    user = User.objects.get(username='admin')
            else:
                user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@test.com'})
                if created:
                    user.set_password(password)
                    user.first_name = nombre.split()[0]
                    user.last_name = nombre.split()[1]
                    user.save()
            
            # Crear perfil asociado (si no es admin puro)
            if username != 'admin':
                perfil, _ = Perfil.objects.get_or_create(usuario=user)
                perfil.rol = rol
                perfil.zona = "Caldas"
                perfil.save()
                perfiles[username] = perfil
            
        log.append("✅ Usuarios y Perfiles creados.")

        # D. Crear Rutas y Asignaciones
        # Ruta para Juan
        ruta_juan, _ = Ruta.objects.get_or_create(
            nombre="Ruta Centro - Juan",
            defaults={
                "fecha_programada": timezone.now().date(),
                "estado": "ACTIVA",
                "lider": perfiles["lider.demo"],
                "asesor_asignado": perfiles["asesor.juan"]
            }
        )
        if not ruta_juan.puntos.exists():
            PuntoVisita.objects.create(ruta=ruta_juan, conjunto=conjuntos_objs[0], orden=1)
            PuntoVisita.objects.create(ruta=ruta_juan, conjunto=conjuntos_objs[1], orden=2)
            log.append("✅ Ruta de Juan asignada.")

        # Ruta para Maria
        ruta_maria, _ = Ruta.objects.get_or_create(
            nombre="Ruta Norte - María",
            defaults={
                "fecha_programada": timezone.now().date(),
                "estado": "ACTIVA",
                "lider": perfiles["lider.demo"],
                "asesor_asignado": perfiles["asesor.maria"]
            }
        )
        if not ruta_maria.puntos.exists():
            PuntoVisita.objects.create(ruta=ruta_maria, conjunto=conjuntos_objs[2], orden=1)
            PuntoVisita.objects.create(ruta=ruta_maria, conjunto=conjuntos_objs[3], orden=2)
            PuntoVisita.objects.create(ruta=ruta_maria, conjunto=conjuntos_objs[4], orden=3)
            log.append("✅ Ruta de María asignada.")

        # Respuesta HTML
        html_response = "<h1>🌱 Base de Datos Poblada con Éxito</h1><ul>"
        for msg in log:
            html_response += f"<li>{msg}</li>"
        html_response += "</ul><br><a href='/admin' style='font-size:20px'>➡️ Ir al Admin</a>"
        
        return HttpResponse(html_response)

    except Exception as e:
        return HttpResponse(f"<h1>❌ Error Crítico:</h1><p>{str(e)}</p>")

# ==============================================================================
# 3. LISTA DE URLS (Rutas)
# ==============================================================================
urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/', include('gestion.urls')),
    
    # Autenticación (Token para Login)
    path('api/token-auth/', token_views.obtain_auth_token),

    # Documentación Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # --- RUTA TEMPORAL DE EMERGENCIA ---
    path('poblar_datos_urgente/', poblar_db_view),
]