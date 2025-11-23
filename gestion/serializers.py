from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, Conjunto, Ruta, PuntoVisita, Visita, Evidencia

# ==============================================================================
# SERIALIZERS DE USUARIO
# ==============================================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'rol', 'telefono', 'zona']

# ==============================================================================
# SERIALIZERS DE GESTIÓN (Conjuntos y Rutas)
# ==============================================================================

class ConjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conjunto
        fields = '__all__'

class PuntoVisitaSerializer(serializers.ModelSerializer):
    conjunto = ConjuntoSerializer(read_only=True)
    conjunto_id = serializers.PrimaryKeyRelatedField(queryset=Conjunto.objects.all(), source='conjunto', write_only=True)

    class Meta:
        model = PuntoVisita
        fields = ['id', 'orden', 'conjunto', 'conjunto_id', 'hora_inicio_estimada']

class RutaSerializer(serializers.ModelSerializer):
    puntos = PuntoVisitaSerializer(many=True, read_only=True)
    asesor_nombre = serializers.CharField(source='asesor_asignado.usuario.get_full_name', read_only=True)

    class Meta:
        model = Ruta
        fields = ['id', 'nombre', 'fecha_programada', 'estado', 'lider', 'asesor_asignado', 'asesor_nombre', 'puntos']

# ==============================================================================
# SERIALIZERS DE EJECUCIÓN (Check-in)
# ==============================================================================

class EvidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidencia
        fields = ['id', 'archivo_foto', 'fecha_captura']

class VisitaSerializer(serializers.ModelSerializer):
    evidencias = EvidenciaSerializer(many=True, read_only=True)
    foto_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Visita
        fields = [
            'id', 'punto_visita', 'asesor', 
            'fecha_hora_checkin', 'latitud_registro', 'longitud_registro', 'precision_gps',
            'estado', 'observaciones', 'evidencias', 'foto_upload'
        ]
        read_only_fields = ['fecha_hora_checkin', 'asesor']

    def create(self, validated_data):
        # 1. Sacar la foto para manejarla aparte
        foto = validated_data.pop('foto_upload', None)
        
        # 2. ASIGNACIÓN MANUAL DEL ASESOR (Aquí está el arreglo)
        # Obtenemos el usuario directamente del contexto de la petición
        request = self.context.get('request')
        if request and hasattr(request.user, 'perfil'):
            validated_data['asesor'] = request.user.perfil
            
        # 3. Crear la visita con los datos (ahora sí incluye el asesor)
        visita = Visita.objects.create(**validated_data)

        # 4. Guardar la evidencia si hay foto
        if foto:
            Evidencia.objects.create(visita=visita, archivo_foto=foto)
        
        return visita