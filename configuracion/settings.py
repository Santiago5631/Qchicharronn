import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-o&^w-82qr1lo&08_$amo$$__6&77#5!k*nc!3jof(916o@@ku)'
DEBUG = True
ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

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

    # Apps del proyecto
    'proyecto_principal.apps.ProyectoPrincipalConfig',
    'categoria.apps.CategoriaConfig',
    'compra.apps.CompraConfig',
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
    "backups.apps.BackupsConfig",
    "clientes.apps.ClientesConfig",

    # aplicaciones extras
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
    'django.contrib.auth.middleware.LoginRequiredMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'configuracion.middleware.RequireLoginMiddleware',
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
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and Media files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "proyecto_principal"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'usuario.Usuario'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Redirects
LOGIN_REDIRECT_URL = '/apps/dashboard/'
ACCOUNT_LOGIN_REDIRECT_URL = '/apps/dashboard'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

# === CONFIGURACIÓN DE ALLAUTH ===
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_FIELDS = ['email']
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_ALLOW_REGISTRATION = False
ACCOUNT_FORMS = {'reset_password': 'usuario.forms.CustomPasswordResetForm'}
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# Email Config
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
# CONFIGURACIÓN DE BACKUPS (GOOGLE DRIVE - OAuth2 con Gmail personal)
# ==============================================================================

# Ruta al JSON de OAuth2 que descargaste de Google Cloud Console
# (tipo "Desktop app", llámalo oauth_credentials.json y ponlo en la raíz)
GOOGLE_OAUTH_CREDS_PATH = os.path.join(BASE_DIR, 'oauth_credentials.json')

# Token generado automáticamente al ejecutar generar_token.py por primera vez
GOOGLE_DRIVE_TOKEN_PATH = os.path.join(BASE_DIR, 'token_drive.pkl')

# Ruta al ejecutable de mysqldump
MYSQLDUMP_PATH = 'mysqldump'

# ID de la carpeta de tu Google Drive personal donde se guardarán los backups
GOOGLE_DRIVE_FOLDER_ID = '1rT9T5DWhwrdEPeh8Ks9jWI1sI0qwHm97'
BACKUP_ENCRYPTION_KEY = config('BACKUP_ENCRYPTION_KEY', default=SECRET_KEY)