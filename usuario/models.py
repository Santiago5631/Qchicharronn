from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para crear usuarios y superusuarios sin username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el email y contraseña dados.
        """
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el email y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuario debe tener is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que usa email como identificador principal.
    """
    # Quitamos username porque autenticamos por email
    username = None

    # Tus campos originales
    nombre = models.CharField(
        _("nombre completo"),
        max_length=100,
        blank=True,
        help_text="Nombre completo del usuario"
    )
    cedula = models.CharField(
        _("cédula"),
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        help_text="Número de cédula (opcional)"
    )
    cargo = models.CharField(
        _("cargo"),
        max_length=50,
        default="operador",
        choices=[
            ('mesero', 'Mesero'),
            ('administrador', 'Administrador'),
            ('cocinero', 'Cocinero'),
            ('parrilla', 'Parrilla'),
        ],
        blank=True,
    )
    numero_celular = models.CharField(
        _("número celular"),
        max_length=20,
        blank=True,
        null=True,
    )
    estado = models.CharField(
        _("estado"),
        max_length=20,
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')],
        default='activo',
    )

    # Campo principal para autenticación
    email = models.EmailField(
        _("correo electrónico"),
        unique=True,
        max_length=255,
        error_messages={
            "unique": _("Ya existe un usuario con este correo electrónico."),
        },
    )

    # Configuración obligatoria para autenticar por email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No pedimos más campos obligatorios al crear superusuario

    # Manager personalizado
    objects = UsuarioManager()

    # Campos útiles que hereda de AbstractUser
    # is_active     → para desactivar cuentas
    # is_staff      → para acceso al admin
    # is_superuser  → para permisos de superusuario
    # date_joined   → fecha de creación
    # last_login    → última sesión

    class Meta:
        verbose_name = _("usuario")
        verbose_name_plural = _("usuarios")
        ordering = ['email']

    def __str__(self):
        return self.email or self.nombre or "Usuario sin nombre"

    def get_full_name(self):
        return self.nombre or self.email

    def get_short_name(self):
        return self.nombre.split()[0] if self.nombre else self.email