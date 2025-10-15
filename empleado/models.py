from django.db import models

class Empleado(models.Model):
    TIPO_CARGO = [
        ('COCINERO', 'Cocinero'),
        ('MESERO', 'Mesero'),
        ('CAJERO', 'Cajero'),
        ('ADMIN', 'Administrador'),
    ]

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(unique=True)
    cargo = models.CharField(max_length=20, choices=TIPO_CARGO)
    fecha_ingreso = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cargo}"
from django.db import models

# Create your models here.
