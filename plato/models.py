from django.db import models
from categoria.models import Categoria
from marca.models import Marca

class Plato(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
from django.db import models

# Create your models here.
