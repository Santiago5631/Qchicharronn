from django.db import models
from django.utils import timezone
from producto.models import Producto
from decimal import Decimal
from django.core.validators import MinValueValidator


class TipoInventario(models.TextChoices):
    """Tipos de control de inventario"""
    PESO = 'peso', 'Por Peso (kg)'
    UNIDAD = 'unidad', 'Por Unidad'


class InventarioDiario(models.Model):
    """Registro diario de inventario"""
    fecha = models.DateField(default=timezone.now)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    numero = models.PositiveIntegerField(default=1)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('abierto', 'Abierto'),
            ('cerrado', 'Cerrado'),
        ],
        default='abierto'
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Inventario Diario'
        verbose_name_plural = 'Inventarios Diarios'
        ordering = ['-fecha']

    def __str__(self):
        return f"Inventario {self.fecha.strftime('%d/%m/%Y')} - {self.get_estado_display()}"

    def cerrar_inventario(self):
        """Cierra el inventario del día"""
        if self.estado == 'cerrado':
            raise ValueError("El inventario ya está cerrado")

        self.estado = 'cerrado'
        self.fecha_cierre = timezone.now()
        self.save()

    def puede_operar(self):
        """Verifica si se puede operar en este inventario"""
        return self.estado == 'abierto'


class MovimientoInventario(models.Model):
    """Detalle de cada producto en el inventario diario"""
    inventario_diario = models.ForeignKey(
        InventarioDiario,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='movimientos_inventario'
    )

    # Tipo de control (heredado del producto)
    tipo_control = models.CharField(
        max_length=10,
        choices=TipoInventario.choices,
        default=TipoInventario.UNIDAD
    )

    # Inventario inicial del día
    inventario_inicial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Stock al inicio del día"
    )

    # Para productos por UNIDAD: descuento automático
    consumo_automatico = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Consumo registrado automáticamente por ventas"
    )

    # Inventario físico al cierre (lo que realmente queda)
    inventario_final = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Stock real al final del día (conteo físico)"
    )

    # Ajustes manuales
    ajuste_manual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Ajuste manual por diferencias, mermas, etc."
    )

    motivo_ajuste = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Razón del ajuste (merma, robo, error, etc.)"
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        unique_together = ['inventario_diario', 'producto']
        ordering = ['producto__nombre']

    def __str__(self):
        return f"{self.producto.nombre} - {self.inventario_diario.fecha}"

    @property
    def consumo_calculado(self):
        """Calcula el consumo real basado en inventario inicial y final"""
        if self.inventario_final is not None:
            return self.inventario_inicial - self.inventario_final
        return Decimal('0.00')

    @property
    def diferencia(self):
        """
        Diferencia entre consumo automático y consumo real
        Positivo = Se consumió más de lo registrado (pérdida)
        Negativo = Se consumió menos (sobra o error)
        """
        if self.tipo_control == TipoInventario.UNIDAD:
            if self.inventario_final is not None:
                consumo_real = self.consumo_calculado
                return consumo_real - self.consumo_automatico
        return Decimal('0.00')

    @property
    def inventario_teorico(self):
        """Inventario que debería quedar según ventas registradas"""
        return self.inventario_inicial - self.consumo_automatico

    def registrar_consumo_venta(self, cantidad):
        """
        Registra el consumo automático cuando se hace una venta
        Solo para productos por UNIDAD
        """
        if self.tipo_control == TipoInventario.UNIDAD:
            self.consumo_automatico += Decimal(str(cantidad))
            self.save()

    def registrar_cierre(self, inventario_final_fisico, motivo_ajuste=None):
        """
        Registra el inventario físico al cierre del día
        """
        if self.inventario_diario.estado == 'cerrado':
            raise ValueError("No se puede modificar un inventario cerrado")

        self.inventario_final = Decimal(str(inventario_final_fisico))

        # Calcular ajuste automático
        if self.tipo_control == TipoInventario.PESO:
            # Para productos por peso, el consumo es la diferencia
            self.ajuste_manual = Decimal('0.00')
        else:
            # Para productos por unidad, el ajuste es la diferencia
            diferencia = self.diferencia
            if diferencia != 0:
                self.ajuste_manual = diferencia
                if motivo_ajuste:
                    self.motivo_ajuste = motivo_ajuste

        self.save()

        # Actualizar stock del producto
        self.producto.stock = self.inventario_final
        self.producto.save()


class HistorialStock(models.Model):
    """Registro histórico de cambios en el stock"""
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='historial_stock'
    )
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=[
            ('entrada', 'Entrada'),
            ('salida', 'Salida'),
            ('ajuste', 'Ajuste'),
            ('cierre', 'Cierre Diario'),
        ]
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    stock_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    stock_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    referencia = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Número de pedido, ajuste, etc."
    )
    observaciones = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Historial de Stock'
        verbose_name_plural = 'Historial de Stock'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.producto.nombre} - {self.get_tipo_movimiento_display()} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
