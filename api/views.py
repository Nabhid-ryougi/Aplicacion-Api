from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario, Departamento, Sensor, Barrera, Evento
from .serializers import (
    UsuarioSerializer, UsuarioListSerializer, DepartamentoSerializer,
    SensorSerializer, BarreraSerializer, EventoSerializer,
    AccesoSensorSerializer, ControlBarreraSerializer
)
from .permissions import IsAdminUser, IsAdminOrReadOnly, IsOwnerOrAdmin


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    Endpoint obligatorio con información del proyecto
    """
    return Response({
        "success": True,
        "data": {
            "autor": ["Dilan - Equipo SmartConnect"],
            "asignatura": "Programación Back End",
            "proyecto": "SmartConnect - Sistema de Control de Acceso Inteligente",
            "descripcion": "API RESTful para gestión de sensores RFID, control de acceso, administración de usuarios y departamentos con sistema de eventos en tiempo real.",
            "version": "1.0",
            "tecnologias": ["Django", "Django Rest Framework", "JWT", "SQLite"],
            "endpoints": {
                "autenticacion": "/api/token/, /api/token/refresh/",
                "usuarios": "/api/usuarios/",
                "departamentos": "/api/departamentos/",
                "sensores": "/api/sensores/",
                "barreras": "/api/barreras/",
                "eventos": "/api/eventos/",
                "acceso": "/api/acceso/sensor/"
            }
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Endpoint para cerrar sesión
    Invalida el refresh token para que no pueda usarse más
    """
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({
                "success": False,
                "error": {
                    "code": 400,
                    "message": "Error de validación",
                    "details": {
                        "refresh": ["Este campo es requerido."]
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            "success": True,
            "message": "Sesión cerrada exitosamente"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "success": False,
            "error": {
                "code": 400,
                "message": "Token inválido o ya expirado",
                "details": str(e)
            }
        }, status=status.HTTP_400_BAD_REQUEST)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Usuarios
    Admin: acceso completo
    Operador: solo puede ver y editar su propio perfil
    """
    queryset = Usuario.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UsuarioListSerializer
        return UsuarioSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if user.rol == 'ADMIN':
            return Usuario.objects.all()
        # Operador solo ve su propio perfil
        return Usuario.objects.filter(id=user.id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Usuario eliminado exitosamente'
        }, status=status.HTTP_200_OK)


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Departamentos
    Admin: acceso completo
    Operador: solo lectura
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Departamento creado exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Departamento actualizado exitosamente',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Departamento eliminado exitosamente'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def sensores(self, request, pk=None):
        """Obtener todos los sensores de un departamento"""
        departamento = self.get_object()
        sensores = departamento.sensores.all()
        serializer = SensorSerializer(sensores, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class SensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Sensores
    Admin: acceso completo
    Operador: solo lectura
    """
    queryset = Sensor.objects.select_related('departamento', 'usuario_asignado').all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Sensor creado exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Sensor actualizado exitosamente',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Sensor eliminado exitosamente'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtener todos los sensores activos"""
        sensores = self.queryset.filter(estado='ACTIVO')
        serializer = self.get_serializer(sensores, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar el estado de un sensor"""
        sensor = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in ['ACTIVO', 'INACTIVO', 'BLOQUEADO', 'PERDIDO']:
            return Response({
                'success': False,
                'error': {
                    'code': 400,
                    'message': 'Estado inválido'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        sensor.estado = nuevo_estado
        sensor.save()
        
        return Response({
            'success': True,
            'message': f'Estado del sensor cambiado a {nuevo_estado}',
            'data': self.get_serializer(sensor).data
        })


class BarreraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Barreras
    Admin: acceso completo
    Operador: solo lectura y control manual
    """
    queryset = Barrera.objects.select_related('departamento').all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Barrera creada exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Barrera actualizada exitosamente',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Barrera eliminada exitosamente'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def controlar(self, request, pk=None):
        """Control manual de barrera (abrir/cerrar)"""
        barrera = self.get_object()
        serializer = ControlBarreraSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        accion = serializer.validated_data['accion']
        descripcion = serializer.validated_data.get('descripcion', f'Control manual: {accion.lower()}')
        
        with transaction.atomic():
            if accion == 'ABRIR':
                barrera.abrir()
                tipo_evento = 'BARRERA_ABIERTA'
            else:
                barrera.cerrar()
                tipo_evento = 'BARRERA_CERRADA'
            
            # Registrar evento
            evento = Evento.objects.create(
                tipo=tipo_evento,
                barrera=barrera,
                usuario_accion=request.user,
                descripcion=descripcion,
                metadata={
                    'accion_manual': True,
                    'usuario': request.user.username
                }
            )
        
        return Response({
            'success': True,
            'message': f'Barrera {accion.lower()}da exitosamente',
            'data': {
                'barrera': self.get_serializer(barrera).data,
                'evento': EventoSerializer(evento).data
            }
        })


class EventoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consulta de Eventos (solo lectura)
    """
    queryset = Evento.objects.select_related('sensor', 'barrera', 'usuario_accion').all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def recientes(self, request):
        """Obtener eventos recientes (últimos 50)"""
        eventos = self.queryset[:50]
        serializer = self.get_serializer(eventos, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Filtrar eventos por tipo"""
        tipo = request.query_params.get('tipo')
        if not tipo:
            return Response({
                'success': False,
                'error': {
                    'code': 400,
                    'message': 'Parámetro "tipo" requerido'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        eventos = self.queryset.filter(tipo=tipo)
        serializer = self.get_serializer(eventos, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acceso_sensor(request):
    """
    Endpoint para simular intento de acceso de un sensor
    Valida el UID, verifica el estado y registra el evento
    """
    serializer = AccesoSensorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    uid = serializer.validated_data['uid']
    departamento_id = serializer.validated_data.get('departamento_id')
    
    try:
        # Buscar sensor por UID
        query = Sensor.objects.select_related('departamento', 'usuario_asignado')
        sensor = query.get(uid=uid)
        
        # Verificar si puede acceder
        puede_acceder = sensor.puede_acceder()
        
        with transaction.atomic():
            if puede_acceder:
                tipo_evento = 'ACCESO_PERMITIDO'
                mensaje = f'Acceso permitido para sensor {sensor.uid}'
                descripcion = f'Sensor {sensor.nombre} ({sensor.uid}) accedió exitosamente al departamento {sensor.departamento.nombre}'
            else:
                tipo_evento = 'ACCESO_DENEGADO'
                mensaje = f'Acceso denegado para sensor {sensor.uid}. Estado: {sensor.get_estado_display()}'
                descripcion = f'Intento de acceso denegado para sensor {sensor.nombre} ({sensor.uid}). Estado del sensor: {sensor.get_estado_display()}'
            
            # Registrar evento
            evento = Evento.objects.create(
                tipo=tipo_evento,
                sensor=sensor,
                descripcion=descripcion,
                metadata={
                    'uid': sensor.uid,
                    'estado_sensor': sensor.estado,
                    'departamento': sensor.departamento.nombre,
                    'usuario_asignado': sensor.usuario_asignado.get_full_name() if sensor.usuario_asignado else None,
                    'timestamp': timezone.now().isoformat()
                }
            )
        
        return Response({
            'success': True,
            'acceso_permitido': puede_acceder,
            'message': mensaje,
            'data': {
                'sensor': SensorSerializer(sensor).data,
                'evento': EventoSerializer(evento).data
            }
        }, status=status.HTTP_200_OK)
        
    except Sensor.DoesNotExist:
        # Sensor no encontrado
        descripcion = f'Intento de acceso con UID no registrado: {uid}'
        
        # Registrar evento de acceso denegado
        evento = Evento.objects.create(
            tipo='ACCESO_DENEGADO',
            descripcion=descripcion,
            metadata={
                'uid': uid,
                'razon': 'UID no registrado',
                'timestamp': timezone.now().isoformat()
            }
        )
        
        return Response({
            'success': False,
            'acceso_permitido': False,
            'error': {
                'code': 404,
                'message': f'Sensor con UID {uid} no encontrado',
                'details': {
                    'evento': EventoSerializer(evento).data
                }
            }
        }, status=status.HTTP_404_NOT_FOUND)
