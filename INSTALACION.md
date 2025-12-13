# 🚀 INSTALACIÓN Y EJECUCIÓN - Windows

## 📋 Requisitos Previos
- Python 3.8 o superior
- Git (opcional)
- Postman o ApiDog (para pruebas)

## ⚡ Instalación Rápida

### Opción 1: Ejecutar Todo de una vez

Abrir PowerShell en la carpeta del proyecto y ejecutar:

```powershell
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
.venv\Scripts\Activate.ps1

# 3. Actualizar pip
python -m pip install --upgrade pip

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear datos de prueba
python crear_datos_prueba.py

# 7. Iniciar servidor
python manage.py runserver
```

### Opción 2: Paso a Paso

#### Paso 1: Crear Entorno Virtual
```powershell
python -m venv .venv
```

#### Paso 2: Activar Entorno Virtual
```powershell
.venv\Scripts\Activate.ps1
```

**Si da error de permisos:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego reintentar la activación.

#### Paso 3: Instalar Dependencias
```powershell
pip install -r requirements.txt
```

#### Paso 4: Configurar Base de Datos
```powershell
python manage.py migrate
```

#### Paso 5: Crear Datos de Prueba
```powershell
python crear_datos_prueba.py
```

**Salida esperada:**
```
============================================================
CREANDO DATOS DE PRUEBA PARA SMARTCONNECT
============================================================

1. Creando usuarios...
   ✓ Usuario Admin creado: admin
   ✓ Usuario Operador creado: operador

2. Creando departamentos...
   ✓ Creado: Entrada Principal
   ...

✓ CREDENCIALES DE ACCESO:
------------------------------------------------------------
ADMIN:
  Usuario: admin
  Contraseña: admin123

OPERADOR:
  Usuario: operador
  Contraseña: operador123
============================================================
```

#### Paso 6: Iniciar Servidor
```powershell
python manage.py runserver
```

**Salida esperada:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 12, 2025 - XX:XX:XX
Django version 5.2.9, using settings 'Aplicacion.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## ✅ Verificación de Instalación

### 1. Abrir navegador en:
```
http://127.0.0.1:8000/api/info/
```

**Deberías ver JSON con información del proyecto.**

### 2. Acceder al panel admin:
```
http://127.0.0.1:8000/admin/
```

**Credenciales:**
- Usuario: `admin`
- Contraseña: `admin123`

### 3. Probar endpoint con PowerShell:
```powershell
curl http://127.0.0.1:8000/api/info/
```

---

## 🔧 Comandos Útiles

### Activar entorno virtual
```powershell
.venv\Scripts\Activate.ps1
```

### Desactivar entorno virtual
```powershell
deactivate
```

### Ver dependencias instaladas
```powershell
pip list
```

### Crear superusuario adicional
```powershell
python manage.py createsuperuser
```

### Crear migraciones (si modificas modelos)
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Recolectar archivos estáticos
```powershell
python manage.py collectstatic
```

### Reiniciar base de datos (⚠️ BORRA TODOS LOS DATOS)
```powershell
# Eliminar base de datos
Remove-Item db.sqlite3

# Eliminar migraciones
Remove-Item -Recurse api\migrations\

# Recrear estructura
New-Item -ItemType Directory -Path api\migrations
New-Item -ItemType File -Path api\migrations\__init__.py

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Recrear datos
python crear_datos_prueba.py
```

---

## 🐛 Solución de Problemas Comunes

### Error: "python no se reconoce como comando"
**Solución:** Instalar Python desde python.org y añadir al PATH

### Error: "No module named 'django'"
**Solución:**
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Execution Policy"
**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Port 8000 is already in use"
**Solución 1:** Usar otro puerto
```powershell
python manage.py runserver 8080
```

**Solución 2:** Matar proceso en puerto 8000
```powershell
# Buscar proceso
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# Matar proceso (reemplazar XXXX con PID)
Stop-Process -Id XXXX -Force
```

### Error: "Access is denied" al activar entorno
**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.venv\Scripts\Activate.ps1
```

---

## 📚 Recursos Adicionales

### Documentación del Proyecto
- `README.md` - Documentación completa
- `DEPLOYMENT_AWS.md` - Guía de despliegue en AWS
- `PRUEBAS_RAPIDAS.md` - Guía de pruebas rápidas
- `RESUMEN_PROYECTO.md` - Resumen ejecutivo

### Colección Postman
- `SmartConnect_API.postman_collection.json` - Importar en Postman/ApiDog

### Archivos Python
- `crear_datos_prueba.py` - Script para generar datos de prueba
- `manage.py` - Utilidad de gestión de Django

---

## 📱 Probar con Postman/ApiDog

### 1. Importar Colección
1. Abrir Postman o ApiDog
2. Clic en "Import"
3. Seleccionar archivo `SmartConnect_API.postman_collection.json`

### 2. Configurar Variables
- Variable: `base_url`
- Valor: `http://127.0.0.1:8000`

### 3. Probar Endpoints
1. Ejecutar "POST Login - Obtener Token (Admin)"
2. El token se guardará automáticamente
3. Probar otros endpoints

---

## 🎯 Siguiente Paso: Desplegar en AWS

Una vez que todo funcione localmente:

1. Leer `DEPLOYMENT_AWS.md`
2. Crear instancia EC2 en AWS
3. Seguir guía paso a paso
4. Probar desde Internet
5. Tomar capturas para entrega

---

## ✅ Checklist de Instalación

- [ ] Python instalado
- [ ] Entorno virtual creado
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Migraciones aplicadas
- [ ] Datos de prueba creados
- [ ] Servidor iniciado
- [ ] Endpoint /api/info/ accesible
- [ ] Panel admin accesible
- [ ] Token JWT obtenido exitosamente
- [ ] Postman configurado (opcional)

---

## 💡 Tips

1. **Siempre activar el entorno virtual** antes de trabajar:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. **Verificar que el servidor esté corriendo** antes de probar:
   ```powershell
   python manage.py runserver
   ```

3. **Usar Postman** para pruebas más fáciles (importar colección JSON)

4. **Revisar logs** si algo falla:
   - Output del servidor en la terminal
   - Archivo `db.sqlite3` contiene los datos

---

## 🚀 ¡Listo!

Si todos los pasos se completaron exitosamente:

✅ API funcionando en `http://127.0.0.1:8000`  
✅ Admin panel en `http://127.0.0.1:8000/admin`  
✅ Datos de prueba creados  
✅ Listo para probar todos los endpoints  

**Ahora puedes continuar con `PRUEBAS_RAPIDAS.md` para probar la API.**

---

**¿Necesitas ayuda?** Revisa:
- `README.md` para documentación completa
- `PRUEBAS_RAPIDAS.md` para ejemplos de uso
- `DEPLOYMENT_AWS.md` para despliegue en producción
