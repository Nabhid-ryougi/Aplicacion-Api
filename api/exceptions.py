from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail
from rest_framework import status
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    """
    Manejador de excepciones personalizado para respuestas consistentes
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': None,
                'details': {}
            }
        }
        
        # Extraer mensaje de error
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['error']['message'] = str(response.data['detail'])
            else:
                # Procesar errores de validación de campos
                custom_response_data['error']['message'] = 'Error de validación'
                custom_response_data['error']['details'] = {}
                
                for field, value in response.data.items():
                    if isinstance(value, list):
                        custom_response_data['error']['details'][field] = [
                            str(v) if isinstance(v, ErrorDetail) else v for v in value
                        ]
                    else:
                        custom_response_data['error']['details'][field] = str(value)
        else:
            custom_response_data['error']['message'] = str(response.data)
        
        # Mensajes específicos según código de estado
        if response.status_code == 401:
            custom_response_data['error']['message'] = custom_response_data['error']['message'] or 'Credenciales de autenticación no proporcionadas o inválidas.'
        elif response.status_code == 403:
            custom_response_data['error']['message'] = custom_response_data['error']['message'] or 'No tienes permisos para realizar esta acción.'
        elif response.status_code == 404:
            custom_response_data['error']['message'] = custom_response_data['error']['message'] or 'Recurso no encontrado.'
        elif response.status_code == 400:
            if not custom_response_data['error']['message']:
                custom_response_data['error']['message'] = 'Datos inválidos.'
        
        response.data = custom_response_data
    
    return response


def handler404(request, exception=None):
    """
    Manejador personalizado para errores 404
    """
    return JsonResponse({
        'success': False,
        'error': {
            'code': 404,
            'message': 'La ruta solicitada no existe.',
            'details': {
                'path': request.path
            }
        }
    }, status=404)


def handler500(request):
    """
    Manejador personalizado para errores 500
    """
    return JsonResponse({
        'success': False,
        'error': {
            'code': 500,
            'message': 'Error interno del servidor.',
            'details': {}
        }
    }, status=500)
