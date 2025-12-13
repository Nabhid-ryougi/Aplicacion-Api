# ⚡ GUÍA RÁPIDA DE PRUEBAS - SmartConnect API

## 🚀 Inicio Rápido (5 minutos)

### 1. Iniciar el Servidor
```bash
cd C:\Users\dilan\Desktop\Api\Aplicacion-Api
.venv\Scripts\activate
python manage.py runserver
```

**Servidor corriendo en:** `http://127.0.0.1:8000`

---

## 🧪 Pruebas Básicas en el Navegador

### ✅ 1. Endpoint de Información (Público - Sin autenticación)
```
http://127.0.0.1:8000/api/info/
```
**Resultado esperado:** JSON con información del proyecto

### ✅ 2. Panel de Administración
```
http://127.0.0.1:8000/admin/
```
**Credenciales:**
- Usuario: `admin`
- Contraseña: `admin123`

### ✅ 3. Error 404 Personalizado
```
http://127.0.0.1:8000/ruta-inexistente/
```
**Resultado esperado:** JSON con mensaje de error personalizado

### ✅ 4. Error 401 (Sin autenticación)
```
http://127.0.0.1:8000/api/usuarios/
```
**Resultado esperado:** JSON con error 401

---

## 🔑 Pruebas con PowerShell (Curl)

### 1. Obtener Token JWT
```powershell
# Admin
curl -X POST http://127.0.0.1:8000/api/token/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"admin\",\"password\":\"admin123\"}'

# Operador
curl -X POST http://127.0.0.1:8000/api/token/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"operador\",\"password\":\"operador123\"}'
```

**Copiar el token `access` de la respuesta para usar en siguientes comandos.**

### 2. Listar Departamentos (Con Token)
```powershell
curl http://127.0.0.1:8000/api/departamentos/ `
  -H "Authorization: Bearer TU-TOKEN-AQUI"
```

### 3. Listar Sensores
```powershell
curl http://127.0.0.1:8000/api/sensores/ `
  -H "Authorization: Bearer TU-TOKEN-AQUI"
```

### 4. Simular Acceso con Sensor ACTIVO (Permitido)
```powershell
curl -X POST http://127.0.0.1:8000/api/acceso/sensor/ `
  -H "Authorization: Bearer TU-TOKEN-AQUI" `
  -H "Content-Type: application/json" `
  -d '{\"uid\":\"RFID-001-ABC\"}'
```

### 5. Simular Acceso con Sensor BLOQUEADO (Denegado)
```powershell
curl -X POST http://127.0.0.1:8000/api/acceso/sensor/ `
  -H "Authorization: Bearer TU-TOKEN-AQUI" `
  -H "Content-Type: application/json" `
  -d '{\"uid\":\"RFID-006-PQR\"}'
```

### 6. Abrir Barrera
```powershell
curl -X POST http://127.0.0.1:8000/api/barreras/1/controlar/ `
  -H "Authorization: Bearer TU-TOKEN-AQUI" `
  -H "Content-Type: application/json" `
  -d '{\"accion\":\"ABRIR\",\"descripcion\":\"Prueba manual\"}'
```

### 7. Cerrar Barrera
```powershell
curl -X POST http://127.0.0.1:8000/api/barreras/1/controlar/ `
  -H "Authorization: Bearer TU-TOKEN-AQUI" `
  -H "Content-Type: application/json" `
  -d '{\"accion\":\"CERRAR\",\"descripcion\":\"Prueba manual\"}'
```

### 8. Ver Eventos Recientes
```powershell
curl http://127.0.0.1:8000/api/eventos/recientes/ `
  -H "Authorization: Bearer TU-TOKEN-AQUI"
```

---

## 📱 Pruebas con Postman/ApiDog

### Paso 1: Importar Colección
1. Abrir Postman o ApiDog
2. Importar archivo: `SmartConnect_API.postman_collection.json`
3. Configurar variable `base_url`: `http://127.0.0.1:8000`

### Paso 2: Obtener Token
1. Ir a carpeta "2. Autenticación"
2. Ejecutar "POST Login - Obtener Token (Admin)" o "POST Login - Obtener Token (Operador)"
3. Los tokens se guardarán automáticamente:
   - `{{token}}` = access token (1 hora de validez)
   - `{{refresh_token}}` = refresh token (7 días de validez)

### Paso 2.1: Cerrar Sesión (Opcional)
1. Para cambiar de usuario, primero cierra sesión con "POST Logout - Cerrar Sesión"
2. Esto invalidará el refresh token actual
3. Luego puedes hacer login con otro usuario sin conflictos

### Paso 3: Probar Endpoints
Todos los endpoints de la colección ya tienen el token configurado automáticamente.

**Pruebas recomendadas en orden:**
1. ✅ GET /api/info/
2. ✅ POST Login (Admin)
3. ✅ GET Listar Departamentos
4. ✅ GET Listar Sensores
5. ✅ POST Simular Acceso (Sensor Activo)
6. ✅ POST Simular Acceso (Sensor Bloqueado)
7. ✅ POST Abrir Barrera
8. ✅ POST Cerrar Barrera
9. ✅ GET Eventos Recientes

---

## 🔒 Pruebas de Seguridad y Errores

### Test 1: Acceso sin token (401)
```powershell
curl http://127.0.0.1:8000/api/usuarios/
```
**Esperado:** Error 401

### Test 2: Operador intenta crear sensor (403)
```powershell
# Primero obtener token de operador
curl -X POST http://127.0.0.1:8000/api/token/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"operador\",\"password\":\"operador123\"}'

# Luego intentar crear (debería fallar)
curl -X POST http://127.0.0.1:8000/api/sensores/ `
  -H "Authorization: Bearer TOKEN-OPERADOR" `
  -H "Content-Type: application/json" `
  -d '{\"uid\":\"TEST\",\"nombre\":\"Test\",\"estado\":\"ACTIVO\",\"departamento\":1}'
```
**Esperado:** Error 403

### Test 3: Recurso no encontrado (404)
```powershell
curl http://127.0.0.1:8000/api/sensores/9999/ `
  -H "Authorization: Bearer TU-TOKEN"
```
**Esperado:** Error 404

### Test 4: Ruta inexistente (404 personalizado)
```powershell
curl http://127.0.0.1:8000/ruta-que-no-existe/
```
**Esperado:** Error 404 con mensaje personalizado

### Test 5: UID duplicado (400)
```powershell
curl -X POST http://127.0.0.1:8000/api/sensores/ `
  -H "Authorization: Bearer TOKEN-ADMIN" `
  -H "Content-Type: application/json" `
  -d '{\"uid\":\"RFID-001-ABC\",\"nombre\":\"Duplicado\",\"estado\":\"ACTIVO\",\"departamento\":1}'
```
**Esperado:** Error 400 con mensaje de validación

---

## 🎯 Escenarios de Prueba Completos

### Escenario 1: Usuario Admin gestiona sensores
```powershell
# 1. Login como admin
$response = curl -X POST http://127.0.0.1:8000/api/token/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"admin\",\"password\":\"admin123\"}'

# 2. Extraer token (guardar manualmente)

# 3. Crear nuevo sensor
curl -X POST http://127.0.0.1:8000/api/sensores/ `
  -H "Authorization: Bearer TU-TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"uid\":\"RFID-100-NEW\",\"nombre\":\"Sensor Nuevo\",\"estado\":\"ACTIVO\",\"departamento\":1}'

# 4. Listar sensores activos
curl http://127.0.0.1:8000/api/sensores/activos/ `
  -H "Authorization: Bearer TU-TOKEN"

# 5. Cambiar estado a bloqueado
curl -X POST http://127.0.0.1:8000/api/sensores/7/cambiar_estado/ `
  -H "Authorization: Bearer TU-TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"estado\":\"BLOQUEADO\"}'
```

### Escenario 2: Simulación de acceso IoT
```powershell
# 1. Intento de acceso con sensor activo
curl -X POST http://127.0.0.1:8000/api/acceso/sensor/ `
  -H "Authorization: Bearer TU-TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"uid\":\"RFID-001-ABC\"}'

# Resultado: Acceso permitido ✅

# 2. Intento de acceso con sensor bloqueado
curl -X POST http://127.0.0.1:8000/api/acceso/sensor/ `
  -H "Authorization: Bearer TU-TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"uid\":\"RFID-006-PQR\"}'

# Resultado: Acceso denegado ❌

# 3. Verificar eventos generados
curl http://127.0.0.1:8000/api/eventos/recientes/ `
  -H "Authorization: Bearer TU-TOKEN"
```

### Escenario 3: Control de barreras
```powershell
# 1. Ver estado actual de barreras
curl http://127.0.0.1:8000/api/barreras/ `
  -H "Authorization: Bearer TU-TOKEN"

# 2. Abrir barrera principal
curl -X POST http://127.0.0.1:8000/api/barreras/1/controlar/ `
  -H "Authorization: Bearer TU-TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"accion\":\"ABRIR\",\"descripcion\":\"Emergencia\"}'

# 3. Verificar evento de apertura
curl http://127.0.0.1:8000/api/eventos/por_tipo/?tipo=BARRERA_ABIERTA `
  -H "Authorization: Bearer TU-TOKEN"

# 4. Cerrar barrera
curl -X POST http://127.0.0.1:8000/api/barreras/1/controlar/ `
  -H "Authorization: Bearer TU-TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"accion\":\"CERRAR\"}'
```

---

## 📊 Datos de Prueba Disponibles

### Usuarios
- **admin** / admin123 (ADMIN)
- **operador** / operador123 (OPERADOR)

### Departamentos
1. Entrada Principal
2. Oficinas Administrativas
3. Laboratorio Técnico
4. Estacionamiento

### Sensores RFID
- `RFID-001-ABC` - **ACTIVO** (Admin)
- `RFID-002-DEF` - **ACTIVO** (Operador)
- `RFID-003-GHI` - **ACTIVO** (Laboratorio)
- `RFID-004-JKL` - **ACTIVO** (Estacionamiento)
- `RFID-005-MNO` - **INACTIVO**
- `RFID-006-PQR` - **BLOQUEADO**

### Barreras
1. Barrera Principal A
2. Barrera Estacionamiento
3. Barrera Laboratorio

---

## 🐛 Solución de Problemas

### Error: "No connection could be made"
**Solución:** Verificar que el servidor esté corriendo
```bash
python manage.py runserver
```

### Error: Token inválido o expirado
**Solución:** Obtener nuevo token
```powershell
curl -X POST http://127.0.0.1:8000/api/token/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"admin\",\"password\":\"admin123\"}'
```

### Error: "Authentication credentials were not provided"
**Solución:** Agregar header de autorización
```
Authorization: Bearer TU-TOKEN
```

---

## ✅ Checklist de Pruebas

Marcar cada prueba completada:

**Endpoints Básicos:**
- [ ] GET /api/info/ (sin auth)
- [ ] POST /api/token/ (login)
- [ ] Panel admin accesible

**CRUD Departamentos:**
- [ ] GET /api/departamentos/
- [ ] POST /api/departamentos/ (solo admin)
- [ ] PUT /api/departamentos/{id}/
- [ ] DELETE /api/departamentos/{id}/

**CRUD Sensores:**
- [ ] GET /api/sensores/
- [ ] POST /api/sensores/ (solo admin)
- [ ] GET /api/sensores/activos/
- [ ] POST /api/sensores/{id}/cambiar_estado/

**Control IoT:**
- [ ] POST /api/acceso/sensor/ (UID activo - permitido)
- [ ] POST /api/acceso/sensor/ (UID bloqueado - denegado)
- [ ] POST /api/acceso/sensor/ (UID no existe - 404)

**Barreras:**
- [ ] GET /api/barreras/
- [ ] POST /api/barreras/{id}/controlar/ (ABRIR)
- [ ] POST /api/barreras/{id}/controlar/ (CERRAR)

**Eventos:**
- [ ] GET /api/eventos/
- [ ] GET /api/eventos/recientes/
- [ ] GET /api/eventos/por_tipo/?tipo=ACCESO_PERMITIDO

**Manejo de Errores:**
- [ ] 401 - Acceso sin token
- [ ] 403 - Operador intenta crear
- [ ] 404 - Recurso no encontrado
- [ ] 404 - Ruta inexistente
- [ ] 400 - Validación (UID duplicado)

---

## 🎯 TODO: Después del Despliegue AWS

1. Cambiar `base_url` a `http://tu-ip-aws`
2. Repetir todas las pruebas desde AWS
3. Tomar capturas de pantalla:
   - Endpoint /api/info/
   - Login exitoso
   - Listados de recursos
   - Simulación de acceso
   - Errores 401, 403, 404
   - Panel admin
4. Documentar IP pública de AWS
5. Entregar proyecto completo

---

**¡Listo para probar!** 🚀

**Servidor local:** http://127.0.0.1:8000  
**Admin panel:** http://127.0.0.1:8000/admin  
**API Info:** http://127.0.0.1:8000/api/info
