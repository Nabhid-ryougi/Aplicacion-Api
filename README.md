# SmartConnect - Sistema de Control de Acceso Inteligente

## 📋 Descripción del Proyecto

API RESTful desarrollada con Django Rest Framework para el manejo de un sistema de control de acceso inteligente utilizando sensores RFID. El sistema permite administrar usuarios, departamentos, sensores, barreras y eventos de acceso con autenticación JWT y permisos diferenciados.

**Autor:** Dilan - Equipo SmartConnect  
**Asignatura:** Programación Back End  
**Versión:** 1.0

---

## 🎯 Características Principales

✅ **Autenticación JWT** - Sistema de autenticación seguro con tokens  
✅ **Sistema de Roles** - Admin (CRUD completo) y Operador (solo lectura)  
✅ **CRUD Completo** - Para todos los modelos del sistema  
✅ **Validaciones Robustas** - Validaciones a nivel de modelo y serializador  
✅ **Manejo de Errores** - Respuestas consistentes (400, 401, 403, 404, 500)  
✅ **Control de Acceso** - Simulación de acceso por UID de sensores RFID  
✅ **Control de Barreras** - Apertura/cierre manual desde API  
✅ **Registro de Eventos** - Trazabilidad completa de todas las acciones  
✅ **Panel Admin** - Interfaz administrativa de Django personalizada  

---

## 🗂️ Estructura del Proyecto

```
Aplicacion-Api/
│
├── api/                          # Aplicación principal
│   ├── models.py                 # Modelos: Usuario, Departamento, Sensor, Barrera, Evento
│   ├── serializers.py            # Serializadores con validaciones
│   ├── views.py                  # ViewSets y endpoints
│   ├── permissions.py            # Permisos personalizados
│   ├── exceptions.py             # Manejadores de excepciones
│   ├── admin.py                  # Configuración del admin
│   ├── urls.py                   # Rutas de la API
│   └── migrations/               # Migraciones de base de datos
│
├── Aplicacion/                   # Configuración del proyecto
│   ├── settings.py               # Configuración principal
│   ├── urls.py                   # URLs principales
│   └── wsgi.py                   # WSGI para producción
│
├── manage.py                     # Utilidad de Django
├── requirements.txt              # Dependencias del proyecto
├── crear_datos_prueba.py         # Script para datos de prueba
└── README.md                     # Este archivo
```

---

## 📦 Modelos del Sistema

### 1. **Usuario** (Usuario personalizado)
- Extiende AbstractUser de Django
- Campos: username, email, rol (ADMIN/OPERADOR), teléfono
- Roles diferenciados para permisos

### 2. **Departamento**
- Representa zonas o áreas físicas
- Campos: nombre, descripción, ubicación, activo
- Validación: nombre único, mínimo 3 caracteres

### 3. **Sensor**
- Sensores RFID (tarjetas o llaveros)
- Campos: UID único, nombre, estado, departamento, usuario_asignado
- Estados: ACTIVO, INACTIVO, BLOQUEADO, PERDIDO
- Validación: UID único, mínimo 3 caracteres

### 4. **Barrera**
- Control de barreras de acceso
- Campos: nombre, departamento, estado
- Estados: ABIERTA, CERRADA
- Métodos: abrir(), cerrar()

### 5. **Evento**
- Registro de todos los eventos del sistema
- Tipos: ACCESO_PERMITIDO, ACCESO_DENEGADO, BARRERA_ABIERTA, BARRERA_CERRADA
- Campos: tipo, sensor, barrera, usuario_accion, descripción, metadata

---

## 🔗 Endpoints de la API

### **Información del Proyecto (Obligatorio)**
```
GET /api/info/
```
**Permisos:** Público (sin autenticación)  
**Descripción:** Devuelve información del proyecto, autor y versión

---

### **Autenticación JWT**

```
POST /api/token/
```
**Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```
**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLC...",
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

```
POST /api/token/refresh/
```
**Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

---

### **Usuarios**

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/usuarios/` | Listar usuarios | Admin: todos / Operador: solo propio |
| GET | `/api/usuarios/{id}/` | Detalle de usuario | Admin / Operador (propio) |
| POST | `/api/usuarios/` | Crear usuario | Solo Admin |
| PUT/PATCH | `/api/usuarios/{id}/` | Actualizar usuario | Admin / Operador (propio) |
| DELETE | `/api/usuarios/{id}/` | Eliminar usuario | Solo Admin |

---

### **Departamentos**

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/departamentos/` | Listar departamentos | Autenticado |
| GET | `/api/departamentos/{id}/` | Detalle de departamento | Autenticado |
| POST | `/api/departamentos/` | Crear departamento | Solo Admin |
| PUT/PATCH | `/api/departamentos/{id}/` | Actualizar departamento | Solo Admin |
| DELETE | `/api/departamentos/{id}/` | Eliminar departamento | Solo Admin |
| GET | `/api/departamentos/{id}/sensores/` | Sensores del departamento | Autenticado |

---

### **Sensores**

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/sensores/` | Listar sensores | Autenticado |
| GET | `/api/sensores/{id}/` | Detalle de sensor | Autenticado |
| POST | `/api/sensores/` | Crear sensor | Solo Admin |
| PUT/PATCH | `/api/sensores/{id}/` | Actualizar sensor | Solo Admin |
| DELETE | `/api/sensores/{id}/` | Eliminar sensor | Solo Admin |
| GET | `/api/sensores/activos/` | Listar sensores activos | Autenticado |
| POST | `/api/sensores/{id}/cambiar_estado/` | Cambiar estado sensor | Solo Admin |

---

### **Barreras**

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/barreras/` | Listar barreras | Autenticado |
| GET | `/api/barreras/{id}/` | Detalle de barrera | Autenticado |
| POST | `/api/barreras/` | Crear barrera | Solo Admin |
| PUT/PATCH | `/api/barreras/{id}/` | Actualizar barrera | Solo Admin |
| DELETE | `/api/barreras/{id}/` | Eliminar barrera | Solo Admin |
| POST | `/api/barreras/{id}/controlar/` | Abrir/cerrar barrera | Autenticado |

**Ejemplo control de barrera:**
```json
POST /api/barreras/1/controlar/
{
  "accion": "ABRIR",
  "descripcion": "Apertura manual de emergencia"
}
```

---

### **Eventos**

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/eventos/` | Listar eventos | Autenticado |
| GET | `/api/eventos/{id}/` | Detalle de evento | Autenticado |
| GET | `/api/eventos/recientes/` | Últimos 50 eventos | Autenticado |
| GET | `/api/eventos/por_tipo/?tipo=ACCESO_PERMITIDO` | Filtrar por tipo | Autenticado |

---

### **Acceso por Sensor (Simulación IoT)**

```
POST /api/acceso/sensor/
```
**Descripción:** Simula un intento de acceso de un sensor RFID

**Body:**
```json
{
  "uid": "RFID-001-ABC",
  "departamento_id": 1
}
```

**Respuesta exitosa (acceso permitido):**
```json
{
  "success": true,
  "acceso_permitido": true,
  "message": "Acceso permitido para sensor RFID-001-ABC",
  "data": {
    "sensor": { /* datos del sensor */ },
    "evento": { /* evento registrado */ }
  }
}
```

**Respuesta denegada (sensor bloqueado/inactivo):**
```json
{
  "success": true,
  "acceso_permitido": false,
  "message": "Acceso denegado para sensor RFID-006-PQR. Estado: Bloqueado",
  "data": {
    "sensor": { /* datos del sensor */ },
    "evento": { /* evento registrado */ }
  }
}
```

---

## 🔒 Sistema de Permisos

### Roles:
- **ADMIN**: Acceso completo (CRUD total en todos los recursos)
- **OPERADOR**: Solo lectura en la mayoría de recursos, puede controlar barreras

### Códigos de Estado HTTP:
- **200**: OK - Solicitud exitosa
- **201**: Created - Recurso creado exitosamente
- **400**: Bad Request - Error de validación
- **401**: Unauthorized - Sin autenticación
- **403**: Forbidden - Sin permisos suficientes
- **404**: Not Found - Recurso no encontrado
- **500**: Internal Server Error - Error del servidor

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-repositorio>
cd Aplicacion-Api
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# o
source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. Crear datos de prueba
```bash
python crear_datos_prueba.py
```

### 6. Ejecutar servidor
```bash
python manage.py runserver
```

La API estará disponible en: `http://127.0.0.1:8000/`

---

## 🧪 Datos de Prueba

### Usuarios creados:

**Administrador:**
- Username: `admin`
- Password: `admin123`
- Rol: ADMIN

**Operador:**
- Username: `operador`
- Password: `operador123`
- Rol: OPERADOR

### Sensores RFID de prueba:
- `RFID-001-ABC` - Activo (Admin)
- `RFID-002-DEF` - Activo (Operador)
- `RFID-003-GHI` - Activo (Laboratorio)
- `RFID-004-JKL` - Activo (Estacionamiento)
- `RFID-005-MNO` - Inactivo
- `RFID-006-PQR` - Bloqueado

---

## 📝 Ejemplos de Uso con Postman/ApiDog

### 1. Obtener Token JWT
```
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### 2. Listar Sensores (con autenticación)
```
GET http://127.0.0.1:8000/api/sensores/
Authorization: Bearer <tu-token-aqui>
```

### 3. Crear Sensor (solo Admin)
```
POST http://127.0.0.1:8000/api/sensores/
Authorization: Bearer <token-admin>
Content-Type: application/json

{
  "uid": "RFID-007-NEW",
  "nombre": "Nuevo Sensor",
  "estado": "ACTIVO",
  "departamento": 1,
  "descripcion": "Sensor de prueba"
}
```

### 4. Simular Acceso de Sensor
```
POST http://127.0.0.1:8000/api/acceso/sensor/
Authorization: Bearer <tu-token>
Content-Type: application/json

{
  "uid": "RFID-001-ABC"
}
```

### 5. Controlar Barrera
```
POST http://127.0.0.1:8000/api/barreras/1/controlar/
Authorization: Bearer <tu-token>
Content-Type: application/json

{
  "accion": "ABRIR",
  "descripcion": "Apertura manual"
}
```

---

## 🌐 Despliegue en AWS

### Preparación para Producción

1. **Actualizar settings.py:**
```python
DEBUG = False
ALLOWED_HOSTS = ['tu-ip-aws.amazonaws.com', 'tu-dominio.com']
```

2. **Configurar base de datos PostgreSQL** (recomendado para producción)

3. **Recolectar archivos estáticos:**
```bash
python manage.py collectstatic
```

### Opciones de Despliegue:

#### **Opción 1: EC2 con Gunicorn + Nginx**

1. Instalar dependencias en EC2:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. Configurar Gunicorn:
```bash
gunicorn Aplicacion.wsgi:application --bind 0.0.0.0:8000
```

3. Configurar Nginx como proxy reverso

#### **Opción 2: Elastic Beanstalk**

1. Crear archivo `.ebextensions/django.config`
2. Desplegar con EB CLI:
```bash
eb init
eb create
eb deploy
```

#### **Opción 3: AWS Lambda + API Gateway** (serverless)

Usar framework Zappa para despliegue serverless

---

## 🔧 Variables de Entorno (Producción)

Crear archivo `.env`:
```
SECRET_KEY=tu-secret-key-segura
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,ip-aws
DATABASE_URL=postgresql://usuario:pass@host:5432/dbname
```

Instalar: `pip install python-decouple`

En `settings.py`:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

## 📊 Panel de Administración

Acceder a: `http://127.0.0.1:8000/admin/`

**Características:**
- Gestión visual de todos los modelos
- Filtros y búsqueda avanzada
- Acciones masivas (bloquear sensores, abrir/cerrar barreras)
- Solo accesible para usuarios con `is_staff=True`

---

## 🧪 Pruebas

### Verificar Endpoint /api/info/
```bash
curl http://127.0.0.1:8000/api/info/
```

### Probar 404 personalizado
```bash
curl http://127.0.0.1:8000/ruta-inexistente/
```

### Probar 401 (sin token)
```bash
curl http://127.0.0.1:8000/api/usuarios/
```

---

## 📚 Tecnologías Utilizadas

- **Python 3.13**
- **Django 5.2**
- **Django Rest Framework 3.14**
- **Simple JWT 5.3** - Autenticación JWT
- **SQLite** (desarrollo) / **PostgreSQL** (producción recomendado)
- **Gunicorn** - Servidor WSGI para producción

---

## 📄 Licencia

Este proyecto fue desarrollado como parte del curso de Programación Back End.

---

## 👨‍💻 Autor

**Dilan - Equipo SmartConnect**  
Proyecto: Sistema de Control de Acceso Inteligente  
Asignatura: Programación Back End  
Versión: 1.0

---

## 📞 Soporte

Para consultas o problemas, revisar:
- Logs del servidor: `python manage.py runserver`
- Admin panel: `/admin/`
- Eventos registrados: `GET /api/eventos/`

---

**¡Importante para AWS!**

No olvides:
1. ✅ Configurar ALLOWED_HOSTS con tu IP/dominio de AWS
2. ✅ Cambiar DEBUG=False en producción
3. ✅ Usar PostgreSQL o MySQL en vez de SQLite
4. ✅ Configurar certificado SSL (HTTPS)
5. ✅ Configurar CORS apropiadamente
6. ✅ Documentar la IP pública de AWS
7. ✅ Tomar capturas de funcionamiento desde AWS

---

**Estado del Proyecto:** ✅ Completado y listo para despliegue
