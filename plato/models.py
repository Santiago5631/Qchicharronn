from django.db import models
from producto.models import Producto


class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)

    productos = models.ManyToManyField(
        Producto,
        through="PlatoProducto",
        related_name="platos"
    )

    def __str__(self):
        return self.nombre


class PlatoProducto(models.Model):
    plato = models.ForeignKey("Plato", on_delete=models.CASCADE)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="platos_producto"
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.producto.nombre} para {self.plato.nombre}"
