from rest_framework import permissions
from .models import Perfil


class IsLider(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un 'Líder'.
    """
    message = "Solo los usuarios con rol 'Líder' pueden realizar esta acción."

    def has_permission(self, request, view):
        # Primero, verificamos si el usuario está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Luego, verificamos si tiene un perfil y si el rol es 'LIDER'
        try:
            # request.user es el modelo 'Usuario'
            perfil = Perfil.objects.get(usuario=request.user)
            # Comparamos el campo 'rol' como definiste en tus modelos
            return perfil.rol == 'LIDER'
        except Perfil.DoesNotExist:
            # Si no tiene perfil, no es un Líder
            return False

class IsAsesor(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un 'Asesor'.
    """
    message = "Solo los usuarios con rol 'Asesor' pueden realizar esta acción."

    def has_permission(self, request, view):
        # Verificamos si el usuario está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verificamos si tiene un perfil y si el rol es 'ASESOR'
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            return perfil.rol == 'ASESOR'
        except Perfil.DoesNotExist:
            return False
