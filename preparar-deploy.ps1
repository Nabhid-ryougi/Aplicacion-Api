# Script para preparar el proyecto para despliegue en AWS desde GitHub
# Ejecutar en PowerShell desde la raíz del proyecto

Write-Host "🚀 Preparando SmartConnect API para despliegue en AWS..." -ForegroundColor Green

# 1. Verificar que estamos en la raíz del proyecto
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: Ejecuta este script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}

# 2. Verificar archivos necesarios
$archivos = @(
    "requirements-prod.txt",
    "deploy.sh",
    ".gitignore",
    "crear_datos_prueba.py"
)

Write-Host "`n📋 Verificando archivos necesarios..." -ForegroundColor Yellow
foreach ($archivo in $archivos) {
    if (Test-Path $archivo) {
        Write-Host "  ✅ $archivo" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $archivo - FALTA" -ForegroundColor Red
    }
}

# 3. Mostrar estado de Git
Write-Host "`n📊 Estado actual de Git:" -ForegroundColor Yellow
git status

# 4. Agregar cambios
Write-Host "`n📦 Agregando cambios..." -ForegroundColor Yellow
git add .

# 5. Commit
Write-Host "`n💾 Creando commit..." -ForegroundColor Yellow
$fecha = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "Deploy ready: SmartConnect API con logout - $fecha"

# 6. Mostrar instrucciones
Write-Host "`n✅ Proyecto listo para subir a GitHub!" -ForegroundColor Green
Write-Host "`n📝 Próximos pasos:" -ForegroundColor Cyan
Write-Host "
1️⃣  Si NO has creado el repositorio en GitHub:
   - Ve a: https://github.com/new
   - Nombre: Aplicacion-Api
   - Privado o Público
   - NO inicializar con README
   - Crear repositorio

2️⃣  Conectar con GitHub:
   git remote add origin https://github.com/TU-USUARIO/Aplicacion-Api.git
   
3️⃣  Subir código:
   git push -u origin main
   
   (Si es repo privado, usa Personal Access Token como contraseña)

4️⃣  En AWS EC2 Ubuntu:
   wget https://raw.githubusercontent.com/TU-USUARIO/Aplicacion-Api/main/deploy.sh
   chmod +x deploy.sh
   bash deploy.sh
   
5️⃣  Prueba tu API:
   http://TU-IP-AWS/api/info/
" -ForegroundColor White

Write-Host "`n🔗 Enlaces útiles:" -ForegroundColor Cyan
Write-Host "  GitHub new repo: https://github.com/new" -ForegroundColor White
Write-Host "  GitHub tokens: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "  AWS EC2 Console: https://console.aws.amazon.com/ec2/" -ForegroundColor White

Write-Host "`n✨ ¡Listo para desplegar!" -ForegroundColor Green
