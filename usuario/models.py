from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
        ('EMPLEADO', 'Empleado'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='CLIENTE')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.tipo})"
from django.db import models

# Create your models here.
