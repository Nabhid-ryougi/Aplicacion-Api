from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError


class Usuario(AbstractUser):
    """
    Modelo de Usuario personalizado con roles
    """
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('OPERADOR', 'Operador'),
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='OPERADOR',
        help_text='Rol del usuario en el sistema'
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono inválido')]
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    
    def es_admin(self):
        return self.rol == 'ADMIN'
    
    def es_operador(self):
        return self.rol == 'OPERADOR'


class Departamento(models.Model):
    """
    Modelo para representar departamentos o zonas físicas
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres')]
    )
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        if self.nombre:
            self.nombre = self.nombre.strip()
            if len(self.nombre) < 3:
                raise ValidationError({'nombre': 'El nombre debe tener al menos 3 caracteres'})


class Sensor(models.Model):
    """
    Modelo para sensores RFID (tarjetas o llaveros)
    """
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('BLOQUEADO', 'Bloqueado'),
        ('PERDIDO', 'Perdido'),
    ]
    
    uid = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='UID/MAC',
        help_text='Código único del sensor RFID',
        validators=[MinLengthValidator(3, 'El UID debe tener al menos 3 caracteres')]
    )
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres')]
    )
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='ACTIVO'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='sensores'
    )
    usuario_asignado = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} ({self.uid})"
    
    def clean(self):
        if self.uid:
            self.uid = self.uid.strip().upper()
        if self.nombre:
            self.nombre = self.nombre.strip()
            if len(self.nombre) < 3:
                raise ValidationError({'nombre': 'El nombre debe tener al menos 3 caracteres'})
    
    def puede_acceder(self):
        """Verifica si el sensor puede acceder"""
        return self.estado == 'ACTIVO'


class Barrera(models.Model):
    """
    Modelo para control de barrera de acceso
    """
    ESTADO_CHOICES = [
        ('ABIERTA', 'Abierta'),
        ('CERRADA', 'Cerrada'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres')]
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='barreras'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='CERRADA'
    )
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Barrera'
        verbose_name_plural = 'Barreras'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"
    
    def abrir(self):
        """Abre la barrera"""
        self.estado = 'ABIERTA'
        self.save()
    
    def cerrar(self):
        """Cierra la barrera"""
        self.estado = 'CERRADA'
        self.save()


class Evento(models.Model):
    """
    Modelo para registrar eventos de acceso
    """
    TIPO_CHOICES = [
        ('ACCESO_PERMITIDO', 'Acceso Permitido'),
        ('ACCESO_DENEGADO', 'Acceso Denegado'),
        ('BARRERA_ABIERTA', 'Barrera Abierta'),
        ('BARRERA_CERRADA', 'Barrera Cerrada'),
    ]
    
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES
    )
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos'
    )
    barrera = models.ForeignKey(
        Barrera,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos'
    )
    usuario_accion = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_realizados',
        help_text='Usuario que realizó la acción manual'
    )
    descripcion = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def clean(self):
        # Validar que eventos de barrera tengan barrera asociada
        if self.tipo in ['BARRERA_ABIERTA', 'BARRERA_CERRADA'] and not self.barrera:
            raise ValidationError({'barrera': 'Los eventos de barrera requieren una barrera asociada'})
        
        # Validar que eventos de acceso tengan sensor asociado
        if self.tipo in ['ACCESO_PERMITIDO', 'ACCESO_DENEGADO'] and not self.sensor:
            raise ValidationError({'sensor': 'Los eventos de acceso requieren un sensor asociado'})
