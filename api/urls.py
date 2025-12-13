from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    api_info, acceso_sensor, logout,
    UsuarioViewSet, DepartamentoViewSet, SensorViewSet,
    BarreraViewSet, EventoViewSet
)

# Router para ViewSets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'barreras', BarreraViewSet, basename='barrera')
router.register(r'eventos', EventoViewSet, basename='evento')

urlpatterns = [
    # Endpoint de información (obligatorio)
    path('info/', api_info, name='api-info'),
    
    # Autenticación JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout, name='logout'),
    
    # Endpoint de acceso por sensor
    path('acceso/sensor/', acceso_sensor, name='acceso-sensor'),
    
    # Incluir rutas del router
    path('', include(router.urls)),
]
