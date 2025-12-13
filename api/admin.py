from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Departamento, Sensor, Barrera, Evento


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Administración personalizada para Usuario
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'fecha_creacion']
    list_filter = ['rol', 'is_active', 'is_staff', 'fecha_creacion']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-fecha_creacion']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol', 'telefono')}),
        ('Fechas', {'fields': ('fecha_creacion', 'fecha_actualizacion')}),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol', 'telefono', 'email', 'first_name', 'last_name')}),
    )


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """
    Administración para Departamento
    """
    list_display = ['nombre', 'ubicacion', 'activo', 'total_sensores', 'total_barreras', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'ubicacion', 'descripcion']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'ubicacion', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def total_sensores(self, obj):
        return obj.sensores.count()
    total_sensores.short_description = 'Sensores'
    
    def total_barreras(self, obj):
        return obj.barreras.count()
    total_barreras.short_description = 'Barreras'


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    """
    Administración para Sensor
    """
    list_display = ['uid', 'nombre', 'estado', 'departamento', 'usuario_asignado', 'fecha_creacion']
    list_filter = ['estado', 'departamento', 'fecha_creacion']
    search_fields = ['uid', 'nombre', 'descripcion']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('uid', 'nombre', 'descripcion', 'estado')
        }),
        ('Asignaciones', {
            'fields': ('departamento', 'usuario_asignado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25


@admin.register(Barrera)
class BarreraAdmin(admin.ModelAdmin):
    """
    Administración para Barrera
    """
    list_display = ['nombre', 'departamento', 'estado', 'fecha_actualizacion']
    list_filter = ['estado', 'departamento', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'departamento', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['abrir_barreras', 'cerrar_barreras']
    
    def abrir_barreras(self, request, queryset):
        count = queryset.update(estado='ABIERTA')
        self.message_user(request, f'{count} barrera(s) abierta(s) exitosamente.')
    abrir_barreras.short_description = 'Abrir barreras seleccionadas'
    
    def cerrar_barreras(self, request, queryset):
        count = queryset.update(estado='CERRADA')
        self.message_user(request, f'{count} barrera(s) cerrada(s) exitosamente.')
    cerrar_barreras.short_description = 'Cerrar barreras seleccionadas'


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """
    Administración para Evento
    """
    list_display = ['tipo', 'sensor_info', 'barrera', 'usuario_accion', 'fecha_hora']
    list_filter = ['tipo', 'fecha_hora']
    search_fields = ['descripcion', 'sensor__uid', 'sensor__nombre', 'barrera__nombre']
    ordering = ['-fecha_hora']
    readonly_fields = ['fecha_hora']
    date_hierarchy = 'fecha_hora'
    
    fieldsets = (
        ('Información del evento', {
            'fields': ('tipo', 'descripcion')
        }),
        ('Referencias', {
            'fields': ('sensor', 'barrera', 'usuario_accion')
        }),
        ('Metadata', {
            'fields': ('metadata', 'fecha_hora'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 50
    
    def sensor_info(self, obj):
        if obj.sensor:
            return f"{obj.sensor.nombre} ({obj.sensor.uid})"
        return "-"
    sensor_info.short_description = 'Sensor'
    
    def has_add_permission(self, request):
        # Los eventos solo se crean automáticamente
        return False
    
    def has_change_permission(self, request, obj=None):
        # Los eventos no se pueden editar
        return False


# Personalizar el sitio de administración
admin.site.site_header = 'SmartConnect - Administración'
admin.site.site_title = 'SmartConnect Admin'
admin.site.index_title = 'Panel de Control'
