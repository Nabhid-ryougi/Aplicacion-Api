from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permiso personalizado: Solo usuarios con rol ADMIN
    """
    message = 'Solo los administradores pueden realizar esta acción.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'ADMIN'


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: Admin para todo, Operador solo lectura
    """
    message = 'No tienes permisos para realizar esta acción. Solo lectura permitida.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin tiene acceso completo
        if request.user.rol == 'ADMIN':
            return True
        
        # Operador solo puede leer (GET, HEAD, OPTIONS)
        if request.user.rol == 'OPERADOR':
            return request.method in permissions.SAFE_METHODS
        
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado: Admin puede todo, Operador solo su propio perfil
    """
    message = 'No tienes permisos para acceder a este recurso.'
    
    def has_object_permission(self, request, view, obj):
        # Admin tiene acceso completo
        if request.user.rol == 'ADMIN':
            return True
        
        # Operador solo puede ver/editar su propio perfil
        if request.user.rol == 'OPERADOR':
            if request.method in permissions.SAFE_METHODS:
                return obj == request.user
            return obj == request.user
        
        return False
