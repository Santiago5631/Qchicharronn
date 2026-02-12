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
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

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
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

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
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#AUTH_USER_MODEL = 'usuario.Usuario'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',        # login normal
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
]

# Redirect después del login
# Redirección después de login normal y después de login con Google/Facebook
LOGIN_REDIRECT_URL = '/apps/usuarios/listar/'                  # cambia esto por tu ruta real
ACCOUNT_LOGIN_REDIRECT_URL = '/apps/usuarios/listar/'          # muy importante esta también
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# === CONFIGURACIÓN PARA LOGIN CON GOOGLE 100% FUNCIONAL ===
ACCOUNT_AUTHENTICATION_METHOD = 'email'        # Se autentica solo por email
ACCOUNT_UNIQUE_EMAIL = True                    # Evita emails duplicados

# ESTA ES LA CLAVE para que el "Olvidé mi contraseña" funcione con cuentas de Google
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# Permite recuperar contraseña incluso si el usuario nunca puso una (solo Google)
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
# Keys reCAPTCHA (obténlas en https://www.google.com/recaptcha/admin)
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
#opcionales
NOCAPTCHA = True    # para reCaptcha v2 "No Captcha"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'FETCH_USERINFO': True,   # ← trae nombre completo
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True   # ← esta línea elimina la página de "Continue"
# Esto evita que aparezca la pantalla de confirmación después de Google
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True

# Para que los emails se vean en la consola mientras estás en desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Q\'chicharron Local <no-reply@qchicharron.local>'
SERVER_EMAIL = 'Q\'chicharron Local <no-reply@qchicharron.local>'

# En producción cambiarás esto por SMTP (Gmail, SendGrid, etc.)
# Pero ahora con console te llega todo a la terminal y es perfecto para probar

MESSAGE_TAGS = {
    messages.DEBUG: "info",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}
