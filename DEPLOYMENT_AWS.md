# 🚀 Guía de Despliegue en AWS - SmartConnect API (Desde GitHub)

## 📋 Índice
1. [Preparación Local](#1-preparación-local)
2. [Subir Proyecto a GitHub](#2-subir-proyecto-a-github)
3. [Configuración de AWS EC2](#3-configuración-de-aws-ec2)
4. [Despliegue Automático](#4-despliegue-automático)
5. [Configuración Manual (Alternativa)](#5-configuración-manual-alternativa)
6. [Verificación y Pruebas](#6-verificación-y-pruebas)
7. [Solución de Problemas](#7-solución-de-problemas)

---

## 1. Preparación Local

### 1.1 Verificar archivos necesarios

Asegúrate de tener estos archivos en tu proyecto:

- ✅ `requirements-prod.txt` - Dependencias para producción
- ✅ `deploy.sh` - Script de despliegue automático
- ✅ `.gitignore` - Archivos a ignorar en Git
- ✅ `crear_datos_prueba.py` - Script para datos iniciales

### 1.2 Actualizar .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/

# Entorno
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## 2. Subir Proyecto a GitHub

### 2.1 Inicializar repositorio Git (si no lo has hecho)

```bash
git init
git add .
git commit -m "Proyecto SmartConnect API listo para despliegue"
```

### 2.2 Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `Aplicacion-Api` o el que prefieras
3. Descripción: "API RESTful SmartConnect - Sistema de Control de Acceso"
4. **Público** o **Privado** (recomendado: Privado)
5. NO inicialices con README (ya tienes archivos)
6. Click en **"Create repository"**

### 2.3 Conectar y subir

```bash
git remote add origin https://github.com/TU-USUARIO/Aplicacion-Api.git
git branch -M main
git push -u origin main
```

**Si el repo es privado**, necesitarás generar un Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Selecciona: `repo` (full control)
4. Copia el token generado
5. Úsalo como contraseña al hacer push

---

## 3. Configuración de AWS EC2

### 3.1 Crear instancia EC2

1. Accede a **AWS Console** → **EC2** → **Launch Instance**

2. **Configuración recomendada:**
   - **Nombre:** `smartconnect-api-server`
   - **AMI:** Ubuntu Server 22.04 LTS (HVM)
   - **Tipo de instancia:** t2.micro (Free Tier) o t2.small
   - **Par de claves (Key pair):**
     - Crear nueva: `smartconnect-key.pem`
     - Guardar en lugar seguro
   
3. **Configurar Security Group:**
   - **Nombre:** `smartconnect-sg`
   - **Reglas de entrada (Inbound rules):**
     ```
     SSH    | TCP | 22   | Tu IP o 0.0.0.0/0
     HTTP   | TCP | 80   | 0.0.0.0/0
     HTTPS  | TCP | 443  | 0.0.0.0/0
     Custom | TCP | 8000 | 0.0.0.0/0 (temporal para pruebas)
     ```

4. **Almacenamiento:** 20 GB (suficiente)

5. Click en **"Launch instance"**

6. **Anotar la IP pública** (aparece en la consola EC2)

### 3.2 Conectarse a la instancia

**En Windows (PowerShell):**
```powershell
# Dar permisos al archivo .pem
icacls smartconnect-key.pem /inheritance:r
icacls smartconnect-key.pem /grant:r "$($env:USERNAME):(R)"

# Conectar via SSH
ssh -i smartconnect-key.pem ubuntu@TU-IP-PUBLICA
```

**En Linux/Mac:**
```bash
chmod 400 smartconnect-key.pem
ssh -i smartconnect-key.pem ubuntu@TU-IP-PUBLICA
```

---

## 4. Despliegue Automático

### 4.1 Método rápido (Script automatizado)

Una vez conectado a tu instancia EC2:

```bash
# 1. Descargar el script de despliegue
wget https://raw.githubusercontent.com/TU-USUARIO/Aplicacion-Api/main/deploy.sh

# 2. Dar permisos de ejecución
chmod +x deploy.sh

# 3. Ejecutar el script
bash deploy.sh
```

El script te pedirá la URL de tu repositorio Git. Ingresa:
```
https://github.com/TU-USUARIO/Aplicacion-Api.git
```

**Si tu repo es privado**, necesitarás autenticarte:
```bash
# Configurar credenciales de Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Al clonar, usa tu Personal Access Token como contraseña
```

### 4.2 El script hace automáticamente:

- ✅ Actualiza el sistema Ubuntu
- ✅ Instala Python 3, pip, nginx, git
- ✅ Clona tu repositorio desde GitHub
- ✅ Crea entorno virtual
- ✅ Instala dependencias Python
- ✅ Genera SECRET_KEY seguro
- ✅ Aplica migraciones
- ✅ Crea datos de prueba
- ✅ Configura Gunicorn como servicio
- ✅ Configura Nginx
- ✅ Configura firewall
- ✅ Inicia todos los servicios

---

## 5. Configuración Manual (Alternativa)
    'ec2-XX-XXX-XXX-XXX.compute-1.amazonaws.com',
    'tu-dominio.com',
    'localhost',
    '127.0.0.1'
]

# CORS para producción
CORS_ALLOWED_ORIGINS = [
    "http://tu-dominio.com",
    "https://tu-dominio.com",
]

# Base de datos (opcional, SQLite funciona pero PostgreSQL es mejor)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'smartconnect_db',
#         'USER': 'admin',
#         'PASSWORD': 'tu-password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### 1.2 Actualizar requirements.txt

Asegurarse que incluya:
```
Django>=5.0,<6.0
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.3.0
django-cors-headers>=4.3.0
python-decouple>=3.8
gunicorn>=21.2.0
psycopg2-binary>=2.9.9  # Si usas PostgreSQL
```

---

## 2. Configuración de AWS EC2

### 2.1 Crear Instancia EC2

1. Ir a AWS Console → EC2
2. Clic en "Launch Instance"
3. Seleccionar AMI: **Ubuntu Server 22.04 LTS**
4. Tipo de instancia: **t2.micro** (capa gratuita) o **t2.small**
5. Crear par de claves (descargar archivo .pem)
6. Configurar Security Group:

**Reglas de entrada requeridas:**

| Tipo | Protocolo | Puerto | Origen | Descripción |
|------|-----------|--------|--------|-------------|
| SSH | TCP | 22 | Mi IP | Acceso SSH |
| HTTP | TCP | 80 | 0.0.0.0/0 | Tráfico web |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Tráfico web seguro |
| Custom TCP | TCP | 8000 | 0.0.0.0/0 | Django dev (temporal) |

7. Lanzar instancia

### 2.2 Conectar a la Instancia

**Windows (PowerShell):**
```powershell
ssh -i "ruta\a\tu-llave.pem" ubuntu@tu-ip-publica
```

**Linux/Mac:**
```bash
chmod 400 tu-llave.pem
ssh -i tu-llave.pem ubuntu@tu-ip-publica
```

---

## 3. Instalación en el Servidor

### 3.1 Actualizar el sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 3.2 Instalar Python y dependencias

```bash
sudo apt install python3 python3-pip python3-venv -y
sudo apt install nginx -y
sudo apt install git -y
```

### 3.3 (Opcional) Instalar PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y

# Configurar base de datos
sudo -u postgres psql
CREATE DATABASE smartconnect_db;
CREATE USER admin WITH PASSWORD 'tu-password';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE smartconnect_db TO admin;
\q
```

### 3.4 Clonar o subir el proyecto

**Opción A: Usando Git**
```bash
cd /home/ubuntu
git clone <https://github.com/Nabhid-ryougi/Aplicacion-Api.git> smartconnect
cd smartconnect
```

**Opción B: Subir archivos con SCP (desde tu PC)**
```bash
# Comprimir proyecto
tar -czf smartconnect.tar.gz Aplicacion-Api/

# Subir a AWS
scp -i tu-llave.pem smartconnect.tar.gz ubuntu@tu-ip-aws:/home/ubuntu/

# En el servidor AWS
tar -xzf smartconnect.tar.gz
cd Aplicacion-Api
```

### 3.5 Configurar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.6 Configurar el proyecto

```bash
# Actualizar ALLOWED_HOSTS en settings.py
nano Aplicacion/settings.py
# Cambiar:
# ALLOWED_HOSTS = ['tu-ip-aws', 'tu-dominio.com']
# DEBUG = False

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Crear datos de prueba
python crear_datos_prueba.py

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### 3.7 Probar el servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

Abrir navegador: `http://tu-ip-aws:8000/api/info/`

**Si funciona, presionar Ctrl+C y continuar.**

---

## 4. Configuración de Gunicorn

### 4.1 Crear archivo de configuración

```bash
nano /home/ubuntu/smartconnect/gunicorn_config.py
```

Contenido:
```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
loglevel = "info"
accesslog = "/home/ubuntu/smartconnect/logs/gunicorn_access.log"
errorlog = "/home/ubuntu/smartconnect/logs/gunicorn_error.log"
capture_output = True
```

### 4.2 Crear directorio de logs

```bash
mkdir -p /home/ubuntu/smartconnect/logs
```

### 4.3 Crear servicio systemd

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Contenido:
```ini
[Unit]
Description=Gunicorn daemon for SmartConnect API
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/smartconnect
Environment="PATH=/home/ubuntu/smartconnect/venv/bin"
ExecStart=/home/ubuntu/smartconnect/venv/bin/gunicorn \
          --config /home/ubuntu/smartconnect/gunicorn_config.py \
          Aplicacion.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4.4 Iniciar Gunicorn

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

---

## 5. Configuración de Nginx

### 5.1 Crear configuración de Nginx

```bash
sudo nano /etc/nginx/sites-available/smartconnect
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-ip-aws tu-dominio.com;

    # Logs
    access_log /var/log/nginx/smartconnect_access.log;
    error_log /var/log/nginx/smartconnect_error.log;

    # Archivos estáticos
    location /static/ {
        alias /home/ubuntu/smartconnect/staticfiles/;
    }

    # Proxy a Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

### 5.2 Activar configuración

```bash
sudo ln -s /etc/nginx/sites-available/smartconnect /etc/nginx/sites-enabled/
sudo nginx -t  # Verificar configuración
sudo systemctl restart nginx
```

### 5.3 Ajustar permisos

```bash
sudo chown -R ubuntu:www-data /home/ubuntu/smartconnect
sudo chmod -R 755 /home/ubuntu/smartconnect
```

---

## 6. Configuración de Seguridad

### 6.1 Configurar Firewall UFW

```bash
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable
sudo ufw status
```

### 6.2 (Opcional) Configurar HTTPS con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

### 6.3 Configurar variables de entorno

```bash
nano /home/ubuntu/smartconnect/.env
```

Contenido:
```
SECRET_KEY=genera-una-clave-secreta-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-ip-aws,tu-dominio.com
```

Actualizar `settings.py`:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

## 7. Verificación y Pruebas

### 7.1 Verificar servicios

```bash
# Estado de Gunicorn
sudo systemctl status gunicorn

# Estado de Nginx
sudo systemctl status nginx

# Ver logs de Gunicorn
tail -f /home/ubuntu/smartconnect/logs/gunicorn_error.log

# Ver logs de Nginx
sudo tail -f /var/log/nginx/smartconnect_error.log
```

### 7.2 Probar Endpoints desde AWS

```bash
# Endpoint de información
curl http://localhost/api/info/

# Obtener token
curl -X POST http://localhost/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Listar sensores (con token)
curl http://localhost/api/sensores/ \
  -H "Authorization: Bearer TU-TOKEN-AQUI"
```

### 7.3 Probar desde tu PC

Reemplazar `localhost` con la IP pública de AWS:

```bash
curl http://tu-ip-aws/api/info/
```

**O desde el navegador:**
```
http://tu-ip-aws/api/info/
http://tu-ip-aws/admin/
```

---

## 🎯 Checklist Final para Entregar

- [ ] API desplegada en AWS y funcionando
- [ ] Endpoint `/api/info/` accesible públicamente
- [ ] Autenticación JWT funcionando desde AWS
- [ ] Todos los endpoints CRUD operativos
- [ ] Manejo de errores (401, 403, 404) funcionando
- [ ] Panel admin accesible
- [ ] IP pública documentada
- [ ] Capturas de pantalla tomadas:
  - [ ] Endpoint `/api/info/`
  - [ ] Login JWT exitoso
  - [ ] Listado de recursos
  - [ ] Error 401 sin token
  - [ ] Error 403 sin permisos
  - [ ] Error 404 ruta inexistente
  - [ ] Panel admin de Django

---

## 🔧 Comandos Útiles

### Reiniciar servicios
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Ver logs en tiempo real
```bash
# Gunicorn
tail -f /home/ubuntu/smartconnect/logs/gunicorn_error.log

# Nginx
sudo tail -f /var/log/nginx/smartconnect_error.log
```

### Actualizar código
```bash
cd /home/ubuntu/smartconnect
git pull  # Si usas Git
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## 🆘 Resolución de Problemas

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status gunicorn

# Si no está corriendo, revisar logs
journalctl -u gunicorn -n 50
```

### Error 403 Forbidden en /static/
```bash
# Ajustar permisos
sudo chown -R ubuntu:www-data /home/ubuntu/smartconnect/staticfiles
sudo chmod -R 755 /home/ubuntu/smartconnect/staticfiles
```

### No puedo conectarme desde Internet
- Verificar Security Group en AWS EC2
- Verificar que el puerto 80 esté abierto
- Verificar firewall UFW: `sudo ufw status`

---

## 📊 Información para Documentar

**Datos a incluir en tu entrega:**

1. **URL Base de la API:** `http://tu-ip-publica-aws`
2. **Endpoint /api/info/:** `http://tu-ip-publica-aws/api/info/`
3. **Panel Admin:** `http://tu-ip-publica-aws/admin/`
4. **Credenciales de prueba:**
   - Admin: `admin` / `admin123`
   - Operador: `operador` / `operador123`

---

## ✅ Proyecto Listo para Entrega

Una vez completados todos los pasos, tu API estará:

✅ Desplegada en AWS  
✅ Accesible públicamente  
✅ Con autenticación JWT  
✅ Con manejo profesional de errores  
✅ Con permisos diferenciados  
✅ Con documentación completa  

**¡Éxito en tu proyecto!** 🚀
