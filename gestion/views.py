from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conjunto, Ruta, Visita
from .serializers import ConjuntoSerializer, RutaSerializer, VisitaSerializer

# ==============================================================================
# VISTAS DE SOLO LECTURA
# ==============================================================================

class ConjuntoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Conjunto.objects.all()
    serializer_class = ConjuntoSerializer
    permission_classes = [permissions.IsAuthenticated]

# ==============================================================================
# VISTAS DE GESTIÓN (Rutas)
# ==============================================================================

class RutaViewSet(viewsets.ModelViewSet):
    serializer_class = RutaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'perfil'):
            return Ruta.objects.all()
        
        if user.perfil.rol == 'LIDER':
            return Ruta.objects.all()
        elif user.perfil.rol == 'ASESOR':
            return Ruta.objects.filter(asesor_asignado=user.perfil)
        
        return Ruta.objects.none()

# ==============================================================================
# VISTAS DE OPERACIÓN (Visitas)
# ==============================================================================

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Nota: Ya no necesitamos perform_create ni create aquí, 
    # el Serializer se encarga de todo.

    @action(detail=False, methods=['get'])
    def mis_visitas_hoy(self, request):
        user = request.user
        if hasattr(user, 'perfil'):
            visitas = Visita.objects.filter(asesor=user.perfil).order_by('-fecha_hora_checkin')
            serializer = self.get_serializer(visitas, many=True)
            return Response(serializer.data)
        return Response([])