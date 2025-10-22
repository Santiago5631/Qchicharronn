from django.db import models
from django.utils import timezone
from plato.models import Plato
from producto.models import Producto


class Pedido(models.Model):
    # Relación a la app de mesas (sin importar dónde esté)
    mesa = models.ForeignKey("mesa.Mesa", on_delete=models.CASCADE)

    # Si tu modelo Menu está en la app 'menus'
    menu = models.ForeignKey("menu.Menu", on_delete=models.CASCADE, default=1)

    fecha = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('entregado', 'Entregado')],
        default='pendiente'
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.id}"

    def calcular_subtotal(self):
        total = sum(detalle.menu.precio * detalle.cantidad for detalle in self.detalles.all())
        self.subtotal = total
        return total

    def save(self, *args, **kwargs):
        self.calcular_subtotal()
        super().save(*args, **kwargs)


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    menu = models.ForeignKey("menu.Menu", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.menu.nombre} (Pedido {self.pedido.id})"


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="pedidos_producto"
    )

    def __str__(self):
        return f"Producto {self.producto.nombre} en pedido {self.pedido.id}"


class PedidoMenu(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    menu = models.ForeignKey(
        "menu.Menu",
        on_delete=models.CASCADE,
        related_name="pedidos_menu"
    )
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad}x {self.menu.nombre} en pedido {self.pedido.id}"