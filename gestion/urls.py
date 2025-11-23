from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConjuntoViewSet, RutaViewSet, VisitaViewSet

router = DefaultRouter()
router.register(r'conjuntos', ConjuntoViewSet)
router.register(r'rutas', RutaViewSet, basename='ruta')
router.register(r'visitas', VisitaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]