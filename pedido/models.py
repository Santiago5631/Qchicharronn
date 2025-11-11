from django.db import models
from django.utils import timezone
from producto.models import Producto  # Importa el producto para conocer el área de preparación
from menu.models import Menu  # O plato si así lo tienes
from django.core.validators import MinValueValidator


# -----------------------------
# MODELO PEDIDO
# -----------------------------
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En preparación'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    mesa = models.CharField(max_length=10)
    fecha = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa}"

    # -----------------------------
    # DIVISIÓN AUTOMÁTICA DE COMANDAS
    # -----------------------------
    def obtener_productos_parrilla(self):
        """Devuelve los productos del pedido que van a la parrilla"""
        return self.detalles.filter(menu__producto__area_preparacion='parrilla')

    def obtener_productos_cocina(self):
        """Devuelve los productos del pedido que van a la cocina"""
        return self.detalles.filter(menu__producto__area_preparacion='cocina')

    def tiene_parrilla(self):
        return self.obtener_productos_parrilla().exists()

    def tiene_cocina(self):
        return self.obtener_productos_cocina().exists()


# -----------------------------
# MODELO DETALLE DEL PEDIDO
# -----------------------------
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return f"{self.menu.nombre} x {self.cantidad}"

    @property
    def area_preparacion(self):
        """Permite acceder directamente al área del producto desde el detalle"""
        return self.menu.producto.area_preparacion if hasattr(self.menu, 'producto') else 'cocina'
