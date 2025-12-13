from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Departamento, Sensor, Barrera, Evento


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 
                  'telefono', 'password', 'password_confirm', 'is_active', 
                  'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs
    
    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre de usuario debe tener al menos 3 caracteres.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Usuario.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UsuarioListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listado de usuarios
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 
                  'is_active', 'fecha_creacion']
        read_only_fields = fields


class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Departamento
    """
    total_sensores = serializers.SerializerMethodField()
    total_barreras = serializers.SerializerMethodField()
    
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'descripcion', 'ubicacion', 'activo', 
                  'total_sensores', 'total_barreras', 'fecha_creacion', 
                  'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_total_sensores(self, obj):
        return obj.sensores.count()
    
    def get_total_barreras(self, obj):
        return obj.barreras.count()
    
    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        
        # Validar unicidad en creación y actualización
        instance_id = self.instance.id if self.instance else None
        if Departamento.objects.exclude(id=instance_id).filter(nombre__iexact=value).exists():
            raise serializers.ValidationError("Ya existe un departamento con este nombre.")
        
        return value


class SensorSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Sensor
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario_asignado.get_full_name', read_only=True)
    
    class Meta:
        model = Sensor
        fields = ['id', 'uid', 'nombre', 'descripcion', 'estado', 'departamento', 
                  'departamento_nombre', 'usuario_asignado', 'usuario_nombre', 
                  'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_uid(self, value):
        value = value.strip().upper()
        if len(value) < 3:
            raise serializers.ValidationError("El UID debe tener al menos 3 caracteres.")
        
        # Validar unicidad
        instance_id = self.instance.id if self.instance else None
        if Sensor.objects.exclude(id=instance_id).filter(uid=value).exists():
            raise serializers.ValidationError("Ya existe un sensor con este UID.")
        
        return value
    
    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return value
    
    def validate_estado(self, value):
        estados_validos = ['ACTIVO', 'INACTIVO', 'BLOQUEADO', 'PERDIDO']
        if value not in estados_validos:
            raise serializers.ValidationError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
        return value


class BarreraSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Barrera
    """
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Barrera
        fields = ['id', 'nombre', 'departamento', 'departamento_nombre', 'estado', 
                  'descripcion', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        
        # Validar unicidad
        instance_id = self.instance.id if self.instance else None
        if Barrera.objects.exclude(id=instance_id).filter(nombre__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una barrera con este nombre.")
        
        return value


class EventoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Evento
    """
    sensor_uid = serializers.CharField(source='sensor.uid', read_only=True)
    sensor_nombre = serializers.CharField(source='sensor.nombre', read_only=True)
    barrera_nombre = serializers.CharField(source='barrera.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario_accion.get_full_name', read_only=True)
    
    class Meta:
        model = Evento
        fields = ['id', 'tipo', 'sensor', 'sensor_uid', 'sensor_nombre', 
                  'barrera', 'barrera_nombre', 'usuario_accion', 'usuario_nombre', 
                  'descripcion', 'metadata', 'fecha_hora']
        read_only_fields = ['id', 'fecha_hora']
    
    def validate(self, attrs):
        tipo = attrs.get('tipo')
        sensor = attrs.get('sensor')
        barrera = attrs.get('barrera')
        
        # Validar que eventos de barrera tengan barrera asociada
        if tipo in ['BARRERA_ABIERTA', 'BARRERA_CERRADA'] and not barrera:
            raise serializers.ValidationError({
                "barrera": "Los eventos de barrera requieren una barrera asociada."
            })
        
        # Validar que eventos de acceso tengan sensor asociado
        if tipo in ['ACCESO_PERMITIDO', 'ACCESO_DENEGADO'] and not sensor:
            raise serializers.ValidationError({
                "sensor": "Los eventos de acceso requieren un sensor asociado."
            })
        
        return attrs


class AccesoSensorSerializer(serializers.Serializer):
    """
    Serializador para validar intentos de acceso por UID
    """
    uid = serializers.CharField(required=True, min_length=3)
    departamento_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_uid(self, value):
        return value.strip().upper()


class ControlBarreraSerializer(serializers.Serializer):
    """
    Serializador para control manual de barrera
    """
    accion = serializers.ChoiceField(choices=['ABRIR', 'CERRAR'], required=True)
    descripcion = serializers.CharField(required=False, allow_blank=True)
