from django.db import models

# Create your models here.
class Unidad(models.Model):
    nombre = models.CharField(max_length=50)  # Ej: kg, L, unidades
    descripcion = models.CharField(max_length=100, blank=True, null=True)  # opcional

    def __str__(self):
        return self.nombre