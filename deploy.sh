#!/bin/bash

# Script de despliegue automatizado para AWS EC2 Ubuntu
# Ejecutar como: bash deploy.sh

echo "🚀 Iniciando despliegue de SmartConnect API en AWS..."

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Actualizar sistema
echo -e "${YELLOW}📦 Actualizando sistema...${NC}"
sudo apt update
sudo apt upgrade -y

# 2. Instalar dependencias del sistema
echo -e "${YELLOW}📦 Instalando dependencias del sistema...${NC}"
sudo apt install -y python3 python3-pip python3-venv nginx git

# 3. Crear directorio para el proyecto
echo -e "${YELLOW}📁 Preparando directorio del proyecto...${NC}"
cd /home/ubuntu
PROJECT_DIR="/home/ubuntu/Aplicacion-Api"

# 4. Clonar o actualizar repositorio
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}🔄 Actualizando repositorio existente...${NC}"
    cd $PROJECT_DIR
    git pull origin main
else
    echo -e "${YELLOW}📥 Clonando repositorio desde GitHub...${NC}"
    read -p "Ingresa la URL de tu repositorio Git: " REPO_URL
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

# 5. Crear y activar entorno virtual
echo -e "${YELLOW}🐍 Configurando entorno virtual Python...${NC}"
python3 -m venv venv
source venv/bin/activate

# 6. Instalar dependencias Python
echo -e "${YELLOW}📦 Instalando dependencias Python...${NC}"
pip install --upgrade pip
pip install -r requirements-prod.txt

# 7. Configurar variables de entorno
echo -e "${YELLOW}⚙️  Configurando variables de entorno...${NC}"
if [ ! -f .env ]; then
    echo "SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
    echo "DEBUG=False" >> .env
    echo "ALLOWED_HOSTS=*" >> .env
    echo -e "${GREEN}✅ Archivo .env creado${NC}"
fi

# 8. Aplicar migraciones
echo -e "${YELLOW}🗄️  Aplicando migraciones de base de datos...${NC}"
python manage.py migrate

# 9. Crear superusuario si no existe
echo -e "${YELLOW}👤 Creando datos de prueba...${NC}"
python crear_datos_prueba.py

# 10. Recolectar archivos estáticos
echo -e "${YELLOW}📦 Recolectando archivos estáticos...${NC}"
python manage.py collectstatic --noinput

# 11. Configurar Gunicorn como servicio
echo -e "${YELLOW}⚙️  Configurando Gunicorn...${NC}"
sudo tee /etc/systemd/system/smartconnect.service > /dev/null <<EOF
[Unit]
Description=SmartConnect API Gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Aplicacion-Api
ExecStart=/home/ubuntu/Aplicacion-Api/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 Aplicacion.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# 12. Configurar Nginx
echo -e "${YELLOW}🌐 Configurando Nginx...${NC}"
sudo tee /etc/nginx/sites-available/smartconnect > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /home/ubuntu/Aplicacion-Api/staticfiles/;
    }
}
EOF

# 13. Activar sitio en Nginx
sudo ln -sf /etc/nginx/sites-available/smartconnect /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 14. Configurar firewall
echo -e "${YELLOW}🔥 Configurando firewall...${NC}"
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

# 15. Iniciar servicios
echo -e "${YELLOW}🚀 Iniciando servicios...${NC}"
sudo systemctl daemon-reload
sudo systemctl start smartconnect
sudo systemctl enable smartconnect
sudo systemctl restart nginx

# 16. Verificar estado
echo -e "${GREEN}✅ Despliegue completado!${NC}"
echo ""
echo "📊 Estado de los servicios:"
sudo systemctl status smartconnect --no-pager
echo ""
echo "🌐 Tu API está disponible en:"
echo "http://$(curl -s ifconfig.me)"
echo ""
echo "📝 Endpoints principales:"
echo "  - http://$(curl -s ifconfig.me)/api/info/"
echo "  - http://$(curl -s ifconfig.me)/api/token/"
echo "  - http://$(curl -s ifconfig.me)/admin/"
echo ""
echo "🔑 Credenciales por defecto:"
echo "  - Admin: admin / admin123"
echo "  - Operador: operador / operador123"
