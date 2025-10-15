from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from decimal import Decimal


class MenuProducto(models.Model):
    """Tabla intermedia entre Menu y Producto"""
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        related_name='menu_productos',
        verbose_name='Menú'
    )
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        related_name='productos_menu',
        verbose_name='Producto'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Cantidad'
    )
    orden = models.PositiveIntegerField(default=0)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto del Menú'
        verbose_name_plural = 'Productos del Menú'
        ordering = ['orden', 'fecha_agregado']
        unique_together = ['menu', 'producto']

    def __str__(self):
        return f"{self.menu.nombre} - {self.producto.nombre} ({self.cantidad})"

    def get_subtotal(self):
        if hasattr(self.producto, 'precio') and self.producto.precio:
            return self.cantidad * self.producto.precio
        return Decimal('0.00')


class Menu(models.Model):
    """Modelo general del Menú (puede incluir productos o platos)"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio_menu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    # Relación polimórfica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('content_type', 'object_id')

    categoria_menu = models.CharField(
        max_length=50,
        choices=[
            ('entrada', 'Entrada'),
            ('plato_principal', 'Plato Principal'),
            ('postre', 'Postre'),
            ('bebida', 'Bebida'),
            ('combo', 'Combo')
        ],
        default='plato_principal'
    )
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    productos = models.ManyToManyField(
        'Producto',
        through='MenuProducto',
        related_name='menus_disponibles',
        blank=True
    )

    class Meta:
        verbose_name = "Ítem del Menú"
        verbose_name_plural = "Ítems del Menú"
        ordering = ['categoria_menu', 'nombre']

    def get_precio_final(self):
        if self.precio_menu:
            base = self.precio_menu
        elif self.precio:
            base = self.precio
        elif hasattr(self.item, 'precio'):
            base = self.item.precio
        else:
            base = 0
        return base - (base * (self.descuento / 100))

    def get_tipo_item(self):
        if self.content_type:
            return self.content_type.model
        return "menu_simple"

    def puede_servirse(self):
        if not self.disponible:
            return False
        if not self.item:
            return True
        if self.get_tipo_item() == 'producto':
            return self.item.stock > 0
        if self.get_tipo_item() == 'plato':
            for plato_producto in self.item.platoproducto_set.all():
                if plato_producto.producto.stock < plato_producto.cantidad:
                    return False
        return True

    def __str__(self):
        return f"{self.nombre} - ${self.get_precio_final()}"
