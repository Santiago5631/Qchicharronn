from django.db import models
from menu.models import Pedido
from decimal import Decimal
from clientes.models import Cliente

class Venta(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    )
    METODO_PAGO_CHOICES = (
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    cliente_factura = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas_facturadas'
    )

    metodo_pago = models.CharField(
        max_length=20,
        choices=METODO_PAGO_CHOICES,
        null=True,
        blank=True
    )

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name='venta'
    )

    numero_factura = models.CharField(max_length=20, unique=True, editable=False)

    cliente_nombre = models.CharField(max_length=200)
    tipo_pedido = models.CharField(max_length=10)
    mesa = models.ForeignKey(
        'mesa.Mesa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    fecha_venta = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )

    class Meta:
        ordering = ['-fecha_venta']

    def save(self, *args, **kwargs):

        if not self.numero_factura:
            ultima = Venta.objects.order_by('-id').first()
            numero = 1 if not ultima else ultima.id + 1
            self.numero_factura = f"FAC-{numero:06d}"

        if self.cliente_factura and not self.cliente_nombre:
            self.cliente_nombre = self.cliente_factura.nombre
            if self.cliente_factura.numero_documento:
                self.cliente_nombre += f" - {self.cliente_factura.numero_documento}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_factura


class VentaItem(models.Model):
    venta = models.ForeignKey(
        Venta,
        related_name='items',
        on_delete=models.CASCADE
    )

    nombre = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
