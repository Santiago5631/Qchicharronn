from django.db import models
from administrador.models import Administrador
from pedido.models import Pedido

class Venta(models.Model):
    METODOS_PAGO = [
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta"),
        ("online", "Online"),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, choices=METODOS_PAGO, default="efectivo")
    estado = models.CharField(max_length=20, choices=[
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("cancelado", "Cancelado"),
    ], default="pendiente")
    admin = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):

        if not self.pk:  # Solo la primera vez que se crea la venta
            for detalle in self.pedido.detallepedido_set.all():
                producto = detalle.producto
                cantidad = detalle.cantidad
                producto.stock = (producto.stock or 0) - cantidad
                producto.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        for detalle in self.pedido.detallepedido_set.all():
            producto = detalle.producto
            cantidad = detalle.cantidad
            producto.stock = (producto.stock or 0) + cantidad
            producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Venta #{self.id} - Pedido {self.pedido.id}"
