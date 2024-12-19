"""
Configuración principal del proyecto Django sistemaHostal.

Este archivo contiene configuraciones básicas y avanzadas para el correcto
funcionamiento del proyecto. Incluye ajustes de seguridad, base de datos,
localización, aplicaciones instaladas, entre otros.
"""
from pathlib import Path
import os
import pymysql

# Inicializar soporte para MySQL
pymysql.install_as_MySQLdb()

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta del proyecto (debe mantenerse privada)
SECRET_KEY = 'django-insecure-w-qe79pl(y83asm$$r%g^=)&&3@fm#v=^28w_mp*l^qxu-b=v0'

# Modo de depuración (desactivar en producción)
DEBUG = True

# Hosts permitidos para acceder al proyecto
ALLOWED_HOSTS = []

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',  # Panel de administración
    'django.contrib.auth',  # Gestión de usuarios y autenticación
    'django.contrib.contenttypes',  # Soporte para contenido genérico
    'django.contrib.sessions',  # Gestión de sesiones
    'django.contrib.messages',  # Sistema de mensajes
    'django.contrib.staticfiles',  # Archivos estáticos
    'gestion',  # Aplicación personalizada para el sistema del hostal
]

# Middleware (gestión de peticiones/respuestas)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de la URL principal
ROOT_URLCONF = 'sistemaHostal.urls'

# Configuración de plantillas HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Carpeta de plantillas personalizadas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de WSGI
WSGI_APPLICATION = 'sistemaHostal.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Motor MySQL
        'NAME': 'gestion-hostal',  # Nombre de la base de datos
        'USER': 'admin',  # Usuario de la base de datos
        'PASSWORD': 'Mundial2020)',  # Contraseña del usuario
        'HOST': 'gestion-hostal.crca8g4em4c3.sa-east-1.rds.amazonaws.com',  # Host del servidor de la base de datos
        'PORT': 3306,  # Puerto de conexión
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de internacionalización
LANGUAGE_CODE = 'en-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuración para claves primarias predeterminadas
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
