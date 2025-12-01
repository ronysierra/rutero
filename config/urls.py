from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views as token_views
from django.http import HttpResponse
from django.contrib.auth.models import User

# ==============================================================================
# CONFIGURACIÓN DE SWAGGER (Documentación Automática)
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
# RUTAS PRINCIPALES
# ==============================================================================
urlpatterns = [
    # 1. Panel Administrativo de Django
    path('admin/', admin.site.urls),
    
    # 2. Endpoints de la API (Conectamos con gestion/urls.py)
    path('api/', include('gestion.urls')),
    
    # 3. Autenticación (Para obtener el Token de Login)
    path('api/token-auth/', token_views.obtain_auth_token),

    # 4. Documentación (Swagger y ReDoc)
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

def crear_superuser(request):
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin1234')
            return HttpResponse("<h1>¡LISTO! Superusuario creado.</h1><p>Usuario: admin</p><p>Clave: admin1234</p>")
        else:
            return HttpResponse("<h1>El usuario 'admin' ya existe.</h1>")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear_admin_urgente/', crear_superuser),
    
    path('api/', include('gestion.urls')),
]