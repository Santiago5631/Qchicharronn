from django.db import models

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    pais_origen = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
