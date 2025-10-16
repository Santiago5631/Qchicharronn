from django.db import models
import datetime
import uuid
from .models import Producto, Proveedor, Unidad
class Compra(models.Model):
    id_factura = models.CharField(max_length=20, primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField(default=datetime.date.today)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.id_factura:
            self.id_factura = str(uuid.uuid4())[:8]

        if self.pk:
            try:
                old = Compra.objects.get(pk=self.pk)
                diferencia = self.cantidad - old.cantidad
                if diferencia != 0:
                    self.producto.stock = (self.producto.stock or 0) + diferencia
                    self.producto.save()
            except Compra.DoesNotExist:

                self.producto.stock = (self.producto.stock or 0) + self.cantidad
                self.producto.save()
        else:
            self.producto.stock = (self.producto.stock or 0) + self.cantidad
            self.producto.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        self.producto.stock = (self.producto.stock or 0) - self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.id_factura
