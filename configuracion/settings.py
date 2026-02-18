"""
Django settings for configuracion project.
"""

import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-o&^w-82qr1lo&08_$amo$$__6&77#5!k*nc!3jof(916o@@ku)'
DEBUG = True
ALLOWED_HOSTS = []

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # captcha
    'captcha',
    'proyecto_principal.apps.ProyectoPrincipalConfig',

    # Tus apps personalizadas
    'administrador.apps.AdministradorConfig',
    'categoria.apps.CategoriaConfig',
    'compra.apps.CompraConfig',
    'empleado.apps.EmpleadoConfig',
    'informe.apps.InformeConfig',
    'marca.apps.MarcaConfig',
    'menu.apps.MenuConfig',
    'mesa.apps.MesaConfig',
    'nomina.apps.NominaConfig',
    'pedido.apps.PedidoConfig',
    'plato.apps.PlatoConfig',
    'producto.apps.ProductoConfig',
    'proveedor.apps.ProveedorConfig',
    'unidad.apps.UnidadConfig',
    'usuario.apps.UsuarioConfig',
    'venta.apps.VentaConfig',
    "inventario.apps.InventarioConfig",

    # aplicaciones extras
    "login",
    "widget_tweaks",
    "django_select2",
    'dbbackup',
    'gdstorage',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configuracion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'proyecto_principal' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'configuracion.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "proyecto_principal" ]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuración de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración de sesión
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'usuario.Usuario'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Redirects
LOGIN_REDIRECT_URL = '/apps/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# === CONFIGURACIÓN DE ALLAUTH ===
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FIELDS = ['email']
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_ALLOW_REGISTRATION = False
ACCOUNT_FORMS = {'reset_password': 'usuario.forms.CustomPasswordResetForm'}
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# Email - Gmail real
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'qchicharron32@gmail.com'
EMAIL_HOST_PASSWORD = 'zqni cgkh qafi unzm'
DEFAULT_FROM_EMAIL = 'Q\'chicharron Local <qchicharron32@gmail.com>'
SERVER_EMAIL = 'qchicharron32@gmail.com'

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True

# Mensajes
MESSAGE_TAGS = {
    messages.DEBUG: "info",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

# ==============================================================================
# SISTEMA PROFESIONAL DE BACKUPS (GOOGLE DRIVE) - CONFIGURACIÓN CORREGIDA
# ==============================================================================

# 1. Credenciales y Carpeta
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(BASE_DIR, 'secrets', 'qchicharron-1761667105817-43035ce4e2fb.json')

# RECOMENDACIÓN: Aquí puedes poner el ID de la carpeta o su nombre exacto
GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = 'Copias de seguridad que chicharron'

# 2. SOLUCIÓN AL ERROR DE CUOTA (403): Delegación de permisos
GOOGLE_DRIVE_STORAGE_SERVICE_ACCOUNT_PERMISSION = {
    'role': 'editor',
    'type': 'user',
    'emailAddress': 'davidsanti5631@gmail.com'  # <--- ¡CAMBIA ESTO POR TU GMAIL!
}

# 3. Almacenamientos
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "dbbackup_drive": {
        "BACKEND": "gdstorage.storage.GoogleDriveStorage",
    },
}

# 4. Configuración de dbbackup
DBBACKUP_STORAGE_ALIAS = 'dbbackup_drive'
DBBACKUP_CLEANUP_KEEP = 7

DBBACKUP_CONNECTORS = {
    'default': {
        'CONNECTOR': 'dbbackup.db.mysql.MysqlDumpConnector',
        'DUMP_COMMAND': r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe',
    }
}
