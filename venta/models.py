from django.db import models
from menu.models import Pedido
from decimal import Decimal
from django.db import transaction


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
        # Verificar si es una venta nueva o si cambió el estado a 'pagado'
        es_nueva = self.pk is None
        estado_anterior = None

        if not es_nueva:
            try:
                estado_anterior = Venta.objects.get(pk=self.pk).estado
            except Venta.DoesNotExist:
                estado_anterior = None

        # Generar número de factura
        if not self.numero_factura:
            ultima = Venta.objects.order_by('-id').first()
            numero = 1 if not ultima else ultima.id + 1
            self.numero_factura = f"FAC-{numero:06d}"

        super().save(*args, **kwargs)

        # Si la venta cambió a 'pagado', reducir el inventario
        if self.estado == 'pagado' and estado_anterior != 'pagado':
            self.reducir_inventario()

    def reducir_inventario(self):
        """Reduce el stock de productos cuando se completa una venta"""
        try:
            # Obtener el pedido asociado
            from pedido.models import PedidoDetalle
            from menu.models import MenuProducto

            # Obtener todos los detalles del pedido
            detalles_pedido = PedidoDetalle.objects.filter(pedido=self.pedido).select_related('menu')

            with transaction.atomic():
                for detalle in detalles_pedido:
                    # Para cada menú en el pedido, obtener sus productos
                    menu_productos = MenuProducto.objects.filter(menu=detalle.menu).select_related('producto')

                    for menu_producto in menu_productos:
                        # Calcular la cantidad total a reducir
                        cantidad_a_reducir = menu_producto.cantidad * detalle.cantidad

                        # Reducir el stock del producto
                        producto = menu_producto.producto
                        if producto.stock >= cantidad_a_reducir:
                            producto.stock -= cantidad_a_reducir
                            producto.save()
                        else:
                            # Si no hay suficiente stock, registrar pero no fallar
                            print(
                                f"Advertencia: Stock insuficiente para {producto.nombre}. Stock actual: {producto.stock}, requerido: {cantidad_a_reducir}")
                            # Reducir hasta 0
                            producto.stock = 0
                            producto.save()
        except Exception as e:
            print(f"Error al reducir inventario: {str(e)}")

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
