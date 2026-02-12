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

    # apps necesarias para allauth
    'django.contrib.sites',  # obligatorio para allauth

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # proveedores sociales
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

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
    #aplicaciones extras
    "login",
    "widget_tweaks",
    "django_select2",
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
            BASE_DIR / 'templates',                    # carpeta raíz (por si la usas después)
            BASE_DIR / 'proyecto_principal' / 'templates',  # ← agrega esta línea
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
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'es'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATICFILES_DIRS = [ BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuración de medios para imágenes
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración de sesión para el carrito
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 horas

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'usuario.Usuario'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # login normal
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
]

# Redirect después del login
LOGIN_REDIRECT_URL = '/apps/usuarios/listar/'
ACCOUNT_LOGIN_REDIRECT_URL = '/apps/usuarios/listar/'
LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'

# === CONFIGURACIÓN MÍNIMA Y SEGURA PARA LOGIN ===
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

# DESACTIVAR REGISTRO PÚBLICO Y SOCIAL LOGINS
ACCOUNT_ALLOW_REGISTRATION = False
ACCOUNT_SIGNUP_FORM_CLASS = None
SOCIALACCOUNT_PROVIDERS = {}  # Desactiva Google, Facebook, etc.

# Recuperación de contraseña
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True

# Email - Gmail real
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'qchicharron32@gmail.com'
EMAIL_HOST_PASSWORD = 'zqni cgkh qafi unzm'
DEFAULT_FROM_EMAIL = 'Q\'chicharron Local <qchicharron32@gmail.com>'
SERVER_EMAIL = 'qchicharron32@gmail.com'

# Mensajes
MESSAGE_TAGS = {
    messages.DEBUG: "info",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}
ACCOUNT_FORMS = {
    'reset_password': 'usuario.forms.CustomPasswordResetForm',
}
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
