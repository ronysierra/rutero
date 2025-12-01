from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestion.models import Perfil, Conjunto, Ruta, PuntoVisita
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Carga datos de prueba iniciales'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Iniciando población de datos...'))

        # 1. Crear Conjuntos
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
        
        self.stdout.write(f'- {len(conjuntos_objs)} Conjuntos creados/verificados.')

        # 2. Crear Usuarios y Perfiles
        usuarios_data = [
            # (Username, Password, Rol, Nombre)
            ("lider.demo", "lider123", "LIDER", "Carlos Líder"),
            ("asesor.juan", "asesor123", "ASESOR", "Juan Pérez"),
            ("asesor.maria", "asesor123", "ASESOR", "María González"),
        ]

        perfiles = {}

        for username, password, rol, nombre in usuarios_data:
            user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@test.com'})
            if created:
                user.set_password(password)
                user.first_name = nombre.split()[0]
                user.last_name = nombre.split()[1]
                user.save()
            
            # Crear o actualizar perfil
            perfil, _ = Perfil.objects.get_or_create(usuario=user)
            perfil.rol = rol
            perfil.zona = "Caldas"
            perfil.save()
            perfiles[username] = perfil
            
        self.stdout.write('- Usuarios creados: lider.demo, asesor.juan, asesor.maria')

        # 3. Crear Rutas y Asignaciones
        
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
        # Asignarle puntos a Juan
        if not ruta_juan.puntos.exists():
            PuntoVisita.objects.create(ruta=ruta_juan, conjunto=conjuntos_objs[0], orden=1)
            PuntoVisita.objects.create(ruta=ruta_juan, conjunto=conjuntos_objs[1], orden=2)

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
        # Asignarle puntos a Maria
        if not ruta_maria.puntos.exists():
            PuntoVisita.objects.create(ruta=ruta_maria, conjunto=conjuntos_objs[2], orden=1)
            PuntoVisita.objects.create(ruta=ruta_maria, conjunto=conjuntos_objs[3], orden=2)
            PuntoVisita.objects.create(ruta=ruta_maria, conjunto=conjuntos_objs[4], orden=3)

        self.stdout.write(self.style.SUCCESS('✅ ¡Base de datos poblada con éxito!'))