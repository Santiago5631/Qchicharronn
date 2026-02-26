# usuario/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuario debe tener is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    username = None

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
            ('cajera', 'Cajera'),          # ← ROL NUEVO
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
    foto_perfil = models.ImageField(         # ← CAMPO NUEVO
        _("foto de perfil"),
        upload_to='perfiles/',
        blank=True,
        null=True,
        help_text="Foto de perfil del usuario"
    )

    email = models.EmailField(
        _("correo electrónico"),
        unique=True,
        max_length=255,
        error_messages={
            "unique": _("Ya existe un usuario con este correo electrónico."),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

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

    def get_foto_url(self):
        """Retorna la URL de la foto o una imagen por defecto."""
        if self.foto_perfil:
            return self.foto_perfil.url
        return '/static/lib/img/default_avatar.png'