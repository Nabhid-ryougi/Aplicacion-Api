"""
Script para crear datos de prueba en la base de datos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Aplicacion.settings')
django.setup()

from api.models import Usuario, Departamento, Sensor, Barrera, Evento
from django.utils import timezone


def crear_datos_prueba():
    print("=" * 60)
    print("CREANDO DATOS DE PRUEBA PARA SMARTCONNECT")
    print("=" * 60)
    
    # 1. Crear usuarios
    print("\n1. Creando usuarios...")
    
    # Admin
    if not Usuario.objects.filter(username='admin').exists():
        admin = Usuario.objects.create_user(
            username='admin',
            email='admin@smartconnect.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            rol='ADMIN',
            telefono='+56912345678',
            is_staff=True,
            is_superuser=True
        )
        print(f"   ✓ Usuario Admin creado: {admin.username}")
    else:
        admin = Usuario.objects.get(username='admin')
        print(f"   - Usuario Admin ya existe: {admin.username}")
    
    # Operador
    if not Usuario.objects.filter(username='operador').exists():
        operador = Usuario.objects.create_user(
            username='operador',
            email='operador@smartconnect.com',
            password='operador123',
            first_name='Juan',
            last_name='Pérez',
            rol='OPERADOR',
            telefono='+56987654321'
        )
        print(f"   ✓ Usuario Operador creado: {operador.username}")
    else:
        operador = Usuario.objects.get(username='operador')
        print(f"   - Usuario Operador ya existe: {operador.username}")
    
    # 2. Crear departamentos
    print("\n2. Creando departamentos...")
    
    departamentos_data = [
        {
            'nombre': 'Entrada Principal',
            'descripcion': 'Acceso principal del edificio',
            'ubicacion': 'Piso 1, Puerta A'
        },
        {
            'nombre': 'Oficinas Administrativas',
            'descripcion': 'Área de administración y gerencia',
            'ubicacion': 'Piso 2'
        },
        {
            'nombre': 'Laboratorio Técnico',
            'descripcion': 'Laboratorio de desarrollo y pruebas',
            'ubicacion': 'Piso 3, Ala Norte'
        },
        {
            'nombre': 'Estacionamiento',
            'descripcion': 'Zona de estacionamiento vehicular',
            'ubicacion': 'Subterráneo'
        }
    ]
    
    departamentos = []
    for dept_data in departamentos_data:
        dept, created = Departamento.objects.get_or_create(
            nombre=dept_data['nombre'],
            defaults={
                'descripcion': dept_data['descripcion'],
                'ubicacion': dept_data['ubicacion']
            }
        )
        departamentos.append(dept)
        status = "✓ Creado" if created else "- Ya existe"
        print(f"   {status}: {dept.nombre}")
    
    # 3. Crear sensores
    print("\n3. Creando sensores RFID...")
    
    sensores_data = [
        {
            'uid': 'RFID-001-ABC',
            'nombre': 'Tarjeta Admin Principal',
            'estado': 'ACTIVO',
            'departamento': departamentos[0],
            'usuario': admin
        },
        {
            'uid': 'RFID-002-DEF',
            'nombre': 'Tarjeta Operador Juan',
            'estado': 'ACTIVO',
            'departamento': departamentos[0],
            'usuario': operador
        },
        {
            'uid': 'RFID-003-GHI',
            'nombre': 'Llavero Laboratorio',
            'estado': 'ACTIVO',
            'departamento': departamentos[2],
            'usuario': admin
        },
        {
            'uid': 'RFID-004-JKL',
            'nombre': 'Tarjeta Estacionamiento',
            'estado': 'ACTIVO',
            'departamento': departamentos[3],
            'usuario': None
        },
        {
            'uid': 'RFID-005-MNO',
            'nombre': 'Tarjeta Temporal',
            'estado': 'INACTIVO',
            'departamento': departamentos[1],
            'usuario': None
        },
        {
            'uid': 'RFID-006-PQR',
            'nombre': 'Tarjeta Bloqueada',
            'estado': 'BLOQUEADO',
            'departamento': departamentos[0],
            'usuario': None
        }
    ]
    
    sensores = []
    for sensor_data in sensores_data:
        sensor, created = Sensor.objects.get_or_create(
            uid=sensor_data['uid'],
            defaults={
                'nombre': sensor_data['nombre'],
                'estado': sensor_data['estado'],
                'departamento': sensor_data['departamento'],
                'usuario_asignado': sensor_data['usuario'],
                'descripcion': f"Sensor {sensor_data['uid']} - {sensor_data['estado']}"
            }
        )
        sensores.append(sensor)
        status = "✓ Creado" if created else "- Ya existe"
        print(f"   {status}: {sensor.uid} ({sensor.get_estado_display()})")
    
    # 4. Crear barreras
    print("\n4. Creando barreras de acceso...")
    
    barreras_data = [
        {
            'nombre': 'Barrera Principal A',
            'departamento': departamentos[0],
            'estado': 'CERRADA',
            'descripcion': 'Barrera de entrada principal'
        },
        {
            'nombre': 'Barrera Estacionamiento',
            'departamento': departamentos[3],
            'estado': 'CERRADA',
            'descripcion': 'Barrera de acceso vehicular'
        },
        {
            'nombre': 'Barrera Laboratorio',
            'departamento': departamentos[2],
            'estado': 'CERRADA',
            'descripcion': 'Barrera de seguridad del laboratorio'
        }
    ]
    
    barreras = []
    for barrera_data in barreras_data:
        barrera, created = Barrera.objects.get_or_create(
            nombre=barrera_data['nombre'],
            defaults={
                'departamento': barrera_data['departamento'],
                'estado': barrera_data['estado'],
                'descripcion': barrera_data['descripcion']
            }
        )
        barreras.append(barrera)
        status = "✓ Creado" if created else "- Ya existe"
        print(f"   {status}: {barrera.nombre} ({barrera.get_estado_display()})")
    
    # 5. Crear eventos de prueba
    print("\n5. Creando eventos de prueba...")
    
    eventos_existentes = Evento.objects.count()
    if eventos_existentes == 0:
        eventos_data = [
            {
                'tipo': 'ACCESO_PERMITIDO',
                'sensor': sensores[0],
                'descripcion': 'Acceso exitoso con tarjeta admin',
                'metadata': {'uid': sensores[0].uid, 'departamento': departamentos[0].nombre}
            },
            {
                'tipo': 'ACCESO_PERMITIDO',
                'sensor': sensores[1],
                'descripcion': 'Acceso exitoso con tarjeta operador',
                'metadata': {'uid': sensores[1].uid, 'departamento': departamentos[0].nombre}
            },
            {
                'tipo': 'ACCESO_DENEGADO',
                'sensor': sensores[4],
                'descripcion': 'Acceso denegado - Tarjeta inactiva',
                'metadata': {'uid': sensores[4].uid, 'estado': 'INACTIVO'}
            },
            {
                'tipo': 'ACCESO_DENEGADO',
                'sensor': sensores[5],
                'descripcion': 'Acceso denegado - Tarjeta bloqueada',
                'metadata': {'uid': sensores[5].uid, 'estado': 'BLOQUEADO'}
            },
            {
                'tipo': 'BARRERA_ABIERTA',
                'barrera': barreras[0],
                'usuario_accion': admin,
                'descripcion': 'Barrera abierta manualmente por admin',
                'metadata': {'accion_manual': True, 'usuario': admin.username}
            },
            {
                'tipo': 'BARRERA_CERRADA',
                'barrera': barreras[0],
                'usuario_accion': admin,
                'descripcion': 'Barrera cerrada manualmente por admin',
                'metadata': {'accion_manual': True, 'usuario': admin.username}
            }
        ]
        
        for evento_data in eventos_data:
            Evento.objects.create(**evento_data)
            print(f"   ✓ Evento creado: {evento_data['tipo']}")
    else:
        print(f"   - Ya existen {eventos_existentes} eventos en la base de datos")
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE DATOS CREADOS")
    print("=" * 60)
    print(f"Usuarios:      {Usuario.objects.count()}")
    print(f"Departamentos: {Departamento.objects.count()}")
    print(f"Sensores:      {Sensor.objects.count()}")
    print(f"Barreras:      {Barrera.objects.count()}")
    print(f"Eventos:       {Evento.objects.count()}")
    print("=" * 60)
    
    print("\n✓ CREDENCIALES DE ACCESO:")
    print("-" * 60)
    print("ADMIN:")
    print("  Usuario: admin")
    print("  Contraseña: admin123")
    print("\nOPERADOR:")
    print("  Usuario: operador")
    print("  Contraseña: operador123")
    print("=" * 60)


if __name__ == '__main__':
    crear_datos_prueba()
