# 📖 SmartConnect API - Índice de Documentación

## 🎯 Bienvenido al Proyecto SmartConnect

Sistema de Control de Acceso Inteligente desarrollado con Django Rest Framework

**Autor:** Dilan - Equipo SmartConnect  
**Asignatura:** Programación Back End  
**Versión:** 1.0  
**Estado:** ✅ Completado y Listo para Despliegue

---

## 🚀 Inicio Rápido

¿Primera vez con el proyecto? Sigue este orden:

1. 📥 **[INSTALACION.md](INSTALACION.md)** - Configurar el proyecto localmente
2. ⚡ **[PRUEBAS_RAPIDAS.md](PRUEBAS_RAPIDAS.md)** - Probar la API funcionando
3. 📚 **[README.md](README.md)** - Documentación completa del proyecto
4. 🌐 **[DEPLOYMENT_AWS.md](DEPLOYMENT_AWS.md)** - Desplegar en AWS

---

## 📂 Guía de Documentación

### 📥 1. INSTALACION.md
**¿Para qué?** Configurar el proyecto en tu PC

**Contenido:**
- ✅ Instalación de dependencias
- ✅ Configuración del entorno virtual
- ✅ Creación de base de datos
- ✅ Generación de datos de prueba
- ✅ Inicio del servidor local
- ✅ Solución de problemas comunes

**Tiempo estimado:** 10 minutos

**[→ Ir a INSTALACION.md](INSTALACION.md)**

---

### ⚡ 2. PRUEBAS_RAPIDAS.md
**¿Para qué?** Probar todos los endpoints de la API

**Contenido:**
- ✅ Pruebas básicas en navegador
- ✅ Comandos curl para PowerShell
- ✅ Guía de uso con Postman/ApiDog
- ✅ Escenarios de prueba completos
- ✅ Pruebas de seguridad y errores
- ✅ Checklist de pruebas

**Tiempo estimado:** 20 minutos

**[→ Ir a PRUEBAS_RAPIDAS.md](PRUEBAS_RAPIDAS.md)**

---

### 📚 3. README.md
**¿Para qué?** Entender completamente el proyecto

**Contenido:**
- ✅ Descripción del proyecto
- ✅ Características principales
- ✅ Estructura del proyecto
- ✅ Modelos del sistema
- ✅ Documentación de todos los endpoints
- ✅ Sistema de permisos
- ✅ Ejemplos de uso
- ✅ Configuración para producción

**Lectura:** 15 minutos

**[→ Ir a README.md](README.md)**

---

### 🌐 4. DEPLOYMENT_AWS.md
**¿Para qué?** Desplegar la API en AWS

**Contenido:**
- ✅ Configuración de EC2
- ✅ Instalación en servidor
- ✅ Configuración de Gunicorn
- ✅ Configuración de Nginx
- ✅ Seguridad y SSL
- ✅ Verificación y pruebas
- ✅ Solución de problemas

**Tiempo estimado:** 60-90 minutos

**[→ Ir a DEPLOYMENT_AWS.md](DEPLOYMENT_AWS.md)**

---

### 📊 5. RESUMEN_PROYECTO.md
**¿Para qué?** Vista general ejecutiva del proyecto

**Contenido:**
- ✅ Cumplimiento de requerimientos
- ✅ Arquitectura del sistema
- ✅ Lista de endpoints
- ✅ Sistema de permisos
- ✅ Métricas del proyecto
- ✅ Checklist final

**Lectura:** 5 minutos

**[→ Ir a RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md)**

---

## 🎯 Rutas Rápidas por Objetivo

### "Quiero instalar y probar localmente"
1. [INSTALACION.md](INSTALACION.md) → Instalar
2. [PRUEBAS_RAPIDAS.md](PRUEBAS_RAPIDAS.md) → Probar

### "Quiero entender el proyecto completo"
1. [RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md) → Vista general
2. [README.md](README.md) → Detalles completos

### "Quiero desplegar en AWS"
1. [DEPLOYMENT_AWS.md](DEPLOYMENT_AWS.md) → Guía paso a paso

### "Quiero probar con Postman"
1. Importar: `SmartConnect_API.postman_collection.json`
2. Seguir: [PRUEBAS_RAPIDAS.md](PRUEBAS_RAPIDAS.md) sección Postman

---

## 📦 Archivos del Proyecto

### Documentación
```
📄 INDEX.md (este archivo)          - Índice de documentación
📄 INSTALACION.md                   - Guía de instalación
📄 PRUEBAS_RAPIDAS.md              - Guía de pruebas
📄 README.md                        - Documentación completa
📄 DEPLOYMENT_AWS.md               - Guía de despliegue AWS
📄 RESUMEN_PROYECTO.md             - Resumen ejecutivo
```

### Código Fuente
```
📁 api/                            - Aplicación principal
   ├── models.py                   - Modelos de datos
   ├── serializers.py              - Serializadores
   ├── views.py                    - Vistas y endpoints
   ├── permissions.py              - Permisos personalizados
   ├── exceptions.py               - Manejo de errores
   ├── admin.py                    - Panel administrativo
   └── urls.py                     - Rutas de la API

📁 Aplicacion/                     - Configuración Django
   ├── settings.py                 - Configuración principal
   ├── urls.py                     - URLs principales
   └── wsgi.py                     - WSGI para producción
```

### Utilidades
```
📄 requirements.txt                - Dependencias Python
📄 manage.py                       - Utilidad Django
📄 crear_datos_prueba.py          - Script de datos de prueba
📄 .gitignore                      - Archivos a ignorar en Git
📄 SmartConnect_API.postman_collection.json - Colección Postman
```

---

## 🎓 Conceptos Clave del Proyecto

### Tecnologías Principales
- **Django 5.2** - Framework web
- **Django Rest Framework** - API RESTful
- **Simple JWT** - Autenticación con tokens
- **SQLite/PostgreSQL** - Base de datos

### Arquitectura
- **Patrón MVT** - Model-View-Template (Django)
- **API RESTful** - Endpoints estándar REST
- **JWT Authentication** - Tokens de acceso seguro
- **Role-Based Permissions** - Permisos por rol

### Funcionalidades
1. **Gestión de Usuarios** - Admin y Operador
2. **Control de Sensores RFID** - Estados y validaciones
3. **Gestión de Departamentos** - Zonas físicas
4. **Control de Barreras** - Apertura/cierre manual
5. **Registro de Eventos** - Trazabilidad completa

---

## 🔑 Credenciales de Prueba

### Usuario Administrador
```
Usuario: admin
Contraseña: admin123
Rol: ADMIN
Permisos: CRUD completo
```

### Usuario Operador
```
Usuario: operador
Contraseña: operador123
Rol: OPERADOR
Permisos: Solo lectura + control barreras
```

---

## 🌐 URLs Importantes

### Local (Desarrollo)
```
API Base:    http://127.0.0.1:8000
Info:        http://127.0.0.1:8000/api/info/
Admin:       http://127.0.0.1:8000/admin/
API Docs:    http://127.0.0.1:8000/api/
```

### AWS (Producción)
```
API Base:    http://tu-ip-aws
Info:        http://tu-ip-aws/api/info/
Admin:       http://tu-ip-aws/admin/
```

---

## 📊 Endpoints Principales

### Autenticación
```
POST /api/token/                   - Obtener token JWT
POST /api/token/refresh/          - Renovar token
```

### Recursos CRUD
```
/api/usuarios/                     - Gestión de usuarios
/api/departamentos/                - Gestión de departamentos
/api/sensores/                     - Gestión de sensores RFID
/api/barreras/                     - Gestión de barreras
/api/eventos/                      - Consulta de eventos
```

### Funciones Especiales
```
POST /api/acceso/sensor/          - Simular acceso IoT
POST /api/barreras/{id}/controlar/ - Control manual barrera
GET  /api/eventos/recientes/      - Últimos eventos
```

---

## ✅ Checklist Completo del Proyecto

### Instalación y Configuración
- [ ] Proyecto instalado localmente
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Base de datos creada
- [ ] Datos de prueba generados
- [ ] Servidor corriendo

### Pruebas Locales
- [ ] Endpoint /api/info/ funciona
- [ ] Login JWT exitoso
- [ ] CRUD de todos los recursos
- [ ] Simulación de acceso IoT
- [ ] Control de barreras
- [ ] Manejo de errores (401, 403, 404)

### Despliegue AWS
- [ ] Instancia EC2 creada
- [ ] Proyecto desplegado
- [ ] Gunicorn configurado
- [ ] Nginx configurado
- [ ] API accesible desde Internet
- [ ] Capturas de pantalla tomadas

### Entrega
- [ ] Documentación completa
- [ ] Código fuente limpio
- [ ] IP pública documentada
- [ ] Capturas incluidas
- [ ] README actualizado

---

## 🆘 Obtener Ayuda

### Problemas de Instalación
→ Ver [INSTALACION.md](INSTALACION.md) sección "Solución de Problemas"

### Problemas de Uso
→ Ver [PRUEBAS_RAPIDAS.md](PRUEBAS_RAPIDAS.md) sección "Solución de Problemas"

### Problemas de Despliegue
→ Ver [DEPLOYMENT_AWS.md](DEPLOYMENT_AWS.md) sección "Resolución de Problemas"

### Información General
→ Ver [README.md](README.md)

---

## 🎯 Próximos Pasos

### Si acabas de clonar el proyecto:
1. ✅ Lee esta página completa
2. ✅ Ve a [INSTALACION.md](INSTALACION.md)
3. ✅ Instala y configura localmente
4. ✅ Prueba con [PRUEBAS_RAPIDAS.md](PRUEBAS_RAPIDAS.md)

### Si ya está funcionando localmente:
1. ✅ Lee [README.md](README.md) completo
2. ✅ Prueba todos los endpoints
3. ✅ Prepara para AWS con [DEPLOYMENT_AWS.md](DEPLOYMENT_AWS.md)

### Si está en AWS:
1. ✅ Verifica todos los endpoints
2. ✅ Toma capturas de pantalla
3. ✅ Documenta la IP pública
4. ✅ Prepara la entrega

---

## 📞 Información del Proyecto

**Nombre:** SmartConnect - Sistema de Control de Acceso Inteligente  
**Autor:** Dilan - Equipo SmartConnect  
**Asignatura:** Programación Back End  
**Tecnologías:** Django, DRF, JWT, PostgreSQL/SQLite  
**Versión:** 1.0  
**Estado:** ✅ Completado  

---

## 📄 Resumen de Documentos

| Documento | Propósito | Tiempo | Orden |
|-----------|-----------|--------|-------|
| INDEX.md | Índice general | 5 min | 0️⃣ |
| INSTALACION.md | Instalar proyecto | 10 min | 1️⃣ |
| PRUEBAS_RAPIDAS.md | Probar API | 20 min | 2️⃣ |
| README.md | Documentación completa | 15 min | 3️⃣ |
| DEPLOYMENT_AWS.md | Desplegar en AWS | 90 min | 4️⃣ |
| RESUMEN_PROYECTO.md | Vista ejecutiva | 5 min | 5️⃣ |

---

## 🚀 ¡Comienza Ahora!

**¿Listo para empezar?**

### Paso 1: Instalación
**[→ Ir a INSTALACION.md](INSTALACION.md)**

### ¿Necesitas un resumen primero?
**[→ Ir a RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md)**

---

**¡Éxito con tu proyecto!** 🎉
