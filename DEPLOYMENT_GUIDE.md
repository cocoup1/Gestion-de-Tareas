# 🚀 Guía Completa de Deployment - Django CRUD App

## �️ Información de Créditos Azure (Respaldo de Facturación)

**Fecha de verificación:** 21 de octubre de 2024  
**Cuenta:** javcastro.mer@outlook.com  
**Suscripción ID:** 55714b8e-eaa6-4ec4-a157-0587dd0533f3

### **Créditos Gratuitos Confirmados:**
- ✅ **Saldo disponible:** $200.00 USD
- ✅ **Política de cobro:** "Sus créditos de Azure se usarán antes que su método de pago predeterminado"
- ✅ **Método de pago:** Visa ****7024 (solo se usará DESPUÉS de agotar los $200)
- ✅ **Estado:** Activo con créditos promocionales

### **Estimación de Costos B1:**
- **SKU B1 Linux:** ~$13 USD/mes
- **⚠️ LIMITACIÓN:** Créditos válidos solo 30 días (hasta 20/11/2025)
- **Duración con créditos:** 30 días máximo
- **Para testing (1-2 semanas):** ~$6-7 USD del crédito gratuito
- **Uso completo (30 días):** ~$13 USD del crédito gratuito

### **Evidencia de Respaldo:**
- Portal Azure muestra "Saldo disponible: 200,00 US$"
- Confirmación de que los créditos se usan ANTES que la tarjeta
- Resource Group eliminado correctamente (sin recursos activos previos)

---

## �📋 Tabla de Contenidos
- [Información de Créditos Azure](#información-de-créditos-azure-respaldo-de-facturación)
- [Información del Proyecto](#información-del-proyecto)
- [Prerrequisitos](#prerrequisitos)
- [Configuración Local](#configuración-local)
- [Preparación para Producción](#preparación-para-producción)
- [Deploy en Render.com](#deploy-en-rendercom)
- [Deploy en Azure](#deploy-en-azure)
- [Configuración de Monitoreo 24/7](#configuración-de-monitoreo-247)
- [Troubleshooting](#troubleshooting)
- [Mantenimiento](#mantenimiento)

---

## 📱 Información del Proyecto

**Proyecto:** Sistema de Gestión de Tareas  
**Framework:** Django 5.2.6  
**Python:** 3.13.6  
**Plataforma de Deploy:** Render.com  
**Monitoreo:** UptimeRobot  
**URL Producción:** https://gestion-de-tareas-ny9l.onrender.com

### 🏗️ Arquitectura del Proyecto
```
📦 ProyectoCrud/
├── 📁 djangocrud/           # Configuración principal
│   ├── settings.py          # Configuraciones de desarrollo/producción
│   ├── urls.py              # URLs principales
│   └── wsgi.py             # WSGI para producción
├── 📁 tasks/               # App principal
│   ├── 📁 templates/       # Templates organizados por componentes
│   │   ├── 📁 components/  # Componentes reutilizables
│   │   │   ├── navbar.html        # Navegación con logo
│   │   │   ├── footer.html        # Footer con redes sociales
│   │   │   └── whatsapp_button.html # Botón flotante WhatsApp
│   │   ├── base.html       # Template base limpio
│   │   ├── home.html       # Landing page profesional
│   │   └── ...            # Otros templates
│   ├── 📁 static/         # Archivos estáticos
│   │   └── 📁 tasks/images/
│   │       └── logo.png    # Logo corporativo
│   └── views.py           # Lógica de negocio
├── requirements.txt       # Dependencias Python
├── build.sh              # Script de build para Render
├── .gitignore            # Archivos ignorados por Git
└── README.md             # Documentación principal
```

---

## 🔧 Prerrequisitos

### Herramientas Necesarias:
- ✅ **Python 3.13.6** o superior
- ✅ **Git** para control de versiones
- ✅ **Cuenta GitHub** (repositorio público/privado)
- ✅ **Cuenta Render.com** (tier gratuito)
- ✅ **Cuenta UptimeRobot** (tier gratuito)

### Conocimientos Técnicos:
- Django básico-intermedio
- Git workflow (branches, pull requests)
- Conceptos de deployment y producción
- Variables de entorno

---

## 💻 Configuración Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/[usuario]/crud_prueba.git
cd crud_prueba
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos Local
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Opcional
```

### 5. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```
**URL Local:** http://127.0.0.1:8000/

---

## 🏭 Preparación para Producción

### 1. Archivo `requirements.txt`
```txt
Django==5.2.6
gunicorn==23.0.0
whitenoise==6.11.0
dj-database-url==2.3.0
psycopg2-binary==2.9.9
```

### 2. Script de Build `build.sh`
```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
```

### 3. Configuración `settings.py` para Producción
```python
import os
import dj_database_url

# DEBUG dinámico basado en variable de entorno
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# SECRET_KEY con fallback para desarrollo
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!xlqskk6ac&kmfs0+5ug&kj4vvc(%a6b30+=$bl#^&aa&x7@uj')

# ALLOWED_HOSTS dinámicos
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if not DEBUG:
    ALLOWED_HOSTS.extend([
        '.render.com',
        '.onrender.com',
    ])

# Base de datos híbrida (SQLite local, PostgreSQL producción)
if 'DATABASE_URL' in os.environ:
    # Producción (Render)
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desarrollo local (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "tasks" / "static",
]

# WhiteNoise para servir archivos estáticos
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 4. Archivo `.gitignore`
```gitignore
# Documentación local
documentacion_*.html

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Static files (generated during deployment)
staticfiles/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# VS Code
.vscode/

# OS generated files
.DS_Store
Thumbs.db
Desktop.ini
```

---

## 🌐 Deploy en Render.com

### Paso 1: Preparar Repositorio
1. **Commit y Push** todos los cambios a GitHub:
```bash
git add .
git commit -m "feat: prepare for production deployment"
git push origin master
```

### Paso 2: Crear Servicio Web en Render
1. Ve a **https://dashboard.render.com**
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio GitHub
4. Configura el servicio:

**Configuración Básica:**
```
Name: gestion-de-tareas
Language: Python 3
Branch: master
Build Command: ./build.sh
Start Command: gunicorn --timeout 120 --workers 2 --bind 0.0.0.0:$PORT djangocrud.wsgi:application
```

### Paso 3: Variables de Entorno
En la sección **Environment Variables** de Render:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `DEBUG` | `false` | Desactivar modo debug en producción |
| `SECRET_KEY` | `[generar-clave-segura]` | Clave secreta de Django |
| `DATABASE_URL` | `[auto-generada-por-render]` | URL de PostgreSQL |

**Generar SECRET_KEY segura:**
```python
import secrets
print(secrets.token_urlsafe(50))
```

### Paso 4: Deploy
1. Haz clic en **"Create Web Service"**
2. Render automáticamente:
   - Clona tu repositorio
   - Instala dependencias
   - Ejecuta migraciones
   - Inicia la aplicación

### Paso 5: Verificar Deploy
- **URL generada:** `https://[nombre-servicio].onrender.com`
- **Logs:** Revisar en el dashboard para errores
- **Estado:** Debe mostrar "Live" cuando esté funcionando

---

## 📊 Configuración de Monitoreo 24/7

### Problema: Render Free Tier "Sleep"
- Las aplicaciones gratuitas se "duermen" después de 15 minutos de inactividad
- Causa errores HTTP 503 cuando alguien visita el sitio
- **Solución:** UptimeRobot para mantener la app activa

### Configuración UptimeRobot

#### Paso 1: Crear Cuenta
1. Ve a **https://uptimerobot.com**
2. Haz clic en **"Sign Up Free"**
3. Completa registro y verifica email

#### Paso 2: Crear Monitor
1. En el dashboard, clic **"+ Add New Monitor"**
2. Configuración:
```
Monitor Type: HTTP(s)
Friendly Name: Gestión de Tareas - Render
URL (or IP): https://gestion-de-tareas-ny9l.onrender.com
Monitoring Interval: 5 minutes
```
3. Haz clic en **"Create Monitor"**

#### Paso 3: Verificar Funcionamiento
- **Dashboard:** Mostrará estado UP/DOWN
- **Uptime %:** Meta >99.9%
- **Notificaciones:** Email automáticos si hay problemas

### Resultado Final
- ✅ App siempre activa (ping cada 5 minutos)
- ✅ No más errores HTTP 503
- ✅ Monitoreo profesional 24/7
- ✅ Alertas automáticas por email

---

## 🔧 Troubleshooting

### Error HTTP 503 "Service Unavailable"
**Causa:** App dormida en Render Free tier  
**Solución:** Configurar UptimeRobot (ver sección anterior)

### Error de Build: "requirements.txt not found"
**Causa:** Archivo requirements.txt ausente o mal ubicado  
**Solución:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "add: requirements.txt"
git push origin master
```

### Error: "collectstatic failed"
**Causa:** Configuración incorrecta de archivos estáticos  
**Solución:** Verificar en settings.py:
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "tasks" / "static"]
```

### Error de Base de Datos en Producción
**Causa:** Migraciones no aplicadas  
**Solución:** Verificar `build.sh` incluye:
```bash
python manage.py migrate
```

### Error: "DisallowedHost"
**Causa:** ALLOWED_HOSTS no incluye dominio de Render  
**Solución:** Agregar en settings.py:
```python
ALLOWED_HOSTS = ['.render.com', '.onrender.com']
```

### Archivos Estáticos No Cargan (CSS/JS/Imágenes)
**Causa:** WhiteNoise mal configurado  
**Solución:** Verificar MIDDLEWARE incluye:
```python
'whitenoise.middleware.WhiteNoiseMiddleware',
```

---

## 🛠️ Mantenimiento

### Monitoreo Regular
- **Revisar UptimeRobot** semanalmente
- **Verificar logs** de Render ante errores
- **Uptime objetivo:** >99.9%

### Actualizaciones de Dependencias
```bash
# Actualizar requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "update: dependencies"
git push origin master
```

### Backup de Base de Datos
- Render PostgreSQL incluye backups automáticos
- **Recomendación:** Export manual mensual para datos críticos

### Scaling (Plan Paid)
Si necesitas mayor rendimiento:
- **Render Pro:** $7/mes - Sin sleep, mejor performance
- **Recursos:** 0.5 CPU, 512MB RAM → 1 CPU, 2GB RAM

---

## 📈 Métricas de Éxito

### Performance Actual
- ✅ **Uptime:** >99.9%
- ✅ **Tiempo de carga:** <3 segundos
- ✅ **Disponibilidad:** 24/7 con UptimeRobot
- ✅ **SSL:** Certificado automático por Render

### Funcionalidades Implementadas
- ✅ **Arquitectura de componentes** (navbar, footer, whatsapp)
- ✅ **UI/UX profesional** con Bootstrap 5
- ✅ **Landing page moderna** con call-to-actions
- ✅ **Responsive design** mobile-first
- ✅ **Integración WhatsApp** para contacto directo

---

## 🎯 Próximos Pasos

### Mejoras Técnicas Planeadas
- [ ] **Deploy en Azure** (comparación de plataformas)
- [ ] **Testing con Pytest** (pruebas unitarias e integración)
- [ ] **Performance testing** con JMeter
- [ ] **Code quality** con SonarQube
- [ ] **CI/CD pipeline** con GitHub Actions

### Mejoras de Producto
- [ ] **URLs reales** para redes sociales
- [ ] **Analytics** con Google Analytics
- [ ] **SEO optimization**
- [ ] **PWA** (Progressive Web App)

---

## ☁️ Deploy en Azure

### **Configuración Inicial Azure**

**Créditos disponibles:** $200 USD (verificado 21/10/2024)

#### **Paso 1: Autenticación**
```bash
# Instalar Azure CLI
winget install Microsoft.AzureCLI

# Login
az login

# Verificar suscripción
az account show
```

#### **Paso 2: Crear Resource Group**
```bash
# Crear grupo de recursos
az group create --name rg-gestion-tareas --location eastus

# Verificar creación
az group list --output table
```

#### **Paso 3: Crear App Service Plan (B1)**
```bash
# Crear plan B1 Linux (~$13/mes del crédito gratuito)
az appservice plan create \
    --name plan-gestion-tareas \
    --resource-group rg-gestion-tareas \
    --sku B1 \
    --is-linux

# Verificar creación
az appservice plan list --output table
```

#### **Paso 4: Crear Web App**
```bash
# Crear Web App con Python 3.11
az webapp create \
    --resource-group rg-gestion-tareas \
    --plan plan-gestion-tareas \
    --name gestion-tareas-django \
    --runtime "PYTHON|3.11"
```

#### **Paso 5: Configurar Deployment desde GitHub**
```bash
# Configurar deployment continuo
az webapp deployment source config \
    --name gestion-tareas-django \
    --resource-group rg-gestion-tareas \
    --repo-url https://github.com/cocoup1/crud_prueba \
    --branch main \
    --manual-integration
```

#### **Paso 6: Variables de Entorno**
```bash
# Configurar settings de producción
az webapp config appsettings set \
    --resource-group rg-gestion-tareas \
    --name gestion-tareas-django \
    --settings DJANGO_SETTINGS_MODULE=djangocrud.settings \
                DEBUG=False \
                ALLOWED_HOSTS="gestion-tareas-django.azurewebsites.net" \
                SECRET_KEY="tu-secret-key-aqui"
```

### **Estimación de Costos Azure**
- **B1 Linux Plan:** ~$13 USD/mes
- **⚠️ Con créditos gratuitos:** Solo 30 días (vence 20/11/2025)
- **Para testing (1-2 semanas):** ~$6-7 del crédito de $200
- **Después del 20/11/2025:** Se cobrará a tarjeta Visa ****7024

### **Monitoreo de Costos**
```bash
# Ver costos actuales
az consumption usage list --output table

# Configurar alerta de presupuesto
az consumption budget create \
    --budget-name "presupuesto-gestion-tareas" \
    --amount 50 \
    --time-grain Monthly
```

---

## 👨‍💻 Información del Desarrollador

**Proyecto desarrollado como demostración de skills full-stack:**
- Django backend con arquitectura profesional
- Frontend moderno y responsive
- Deploy en cloud con monitoreo 24/7
- Git workflow con branches y pull requests
- Documentación técnica completa

---

## 📞 Soporte

Para preguntas técnicas o mejoras al proyecto:
- **WhatsApp:** [+56989108136](https://wa.me/+56989108136)
- **Email:** [Configurar según necesidad]
- **GitHub Issues:** Para reportar bugs o sugerir mejoras

---

*Documentación actualizada: Octubre 2025*  
*Versión del proyecto: 1.0.0*