from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.conf import settings



class Menu(models.Model):
    """Modelo simplificado del Menú - Solo productos"""
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Menú')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')

    categoria_menu = models.ForeignKey(
        "categoria.Categoria",
        on_delete=models.PROTECT,
        related_name='menus',
        verbose_name='Categoría',
        null=True,
        blank=True
    )
    precio_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Precio Base',
        default=Decimal('0.01')
    )
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal(0.00),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Descuento (%)',
    )
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    imagen = models.ImageField(upload_to='menus/', blank=True, null=True, verbose_name='Imagen')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')

    # Relación con productos
    productos = models.ManyToManyField(
        'producto.Producto',
        through='MenuProducto',
        related_name='menus_asociados',
        blank=True
    )

    class Meta:
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ['-fecha_creacion', 'categoria_menu', 'nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.get_precio_final()}"

    def get_precio_final(self):
        """Calcula el precio final aplicando descuento"""
        descuento_decimal = self.descuento / 100
        precio_con_descuento = self.precio_base * (1 - descuento_decimal)
        return round(precio_con_descuento, 2)

    def get_total_productos(self):
        """Retorna el número total de productos en este menú"""
        return self.menu_productos.count()

    def puede_servirse(self):
        """Verifica si todos los productos tienen stock disponible"""
        if not self.disponible:
            return False

        for menu_producto in self.menu_productos.all():
            if menu_producto.producto.stock < menu_producto.cantidad:
                return False
        return True


class MenuProducto(models.Model):
    """Tabla intermedia entre Menu y Producto"""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='menu_productos',
        verbose_name='Menú'
    )
    producto = models.ForeignKey(
        'producto.Producto',
        on_delete=models.CASCADE,
        related_name='productos_en_menu',
        verbose_name='Producto'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Cantidad'
    )
    orden = models.PositiveIntegerField(default=0, verbose_name='Orden de Presentación')
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto del Menú'
        verbose_name_plural = 'Productos del Menú'
        ordering = ['orden', 'fecha_agregado']
        unique_together = ['menu', 'producto']

    def __str__(self):
        return f"{self.menu.nombre} - {self.producto.nombre} (x{self.cantidad})"

    def get_subtotal(self):
        """Calcula el subtotal del producto"""
        if hasattr(self.producto, 'precio') and self.producto.precio:
            return self.cantidad * self.producto.precio
        return Decimal('0.00')


class Pedido(models.Model):
    """Modelo para gestionar pedidos/órdenes de menús"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'En Preparación'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    numero_pedido = models.CharField(max_length=20, unique=True, editable=False)
    cliente_nombre = models.CharField(max_length=200, verbose_name='Nombre del Cliente')
    TIPO_PEDIDO_CHOICES = (
        ('mesa', 'En mesa'),
        ('llevar', 'Para llevar'),
    )

    tipo_pedido = models.CharField(
        max_length=10,
        choices=TIPO_PEDIDO_CHOICES,
        default='mesa'
    )
    mesero = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name='Mesero',
        null = True,  # 👈 AGREGAR ESTO
        blank = True
    )

    mesa = models.ForeignKey(
        'mesa.Mesa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,

    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descuento_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Pedido #{self.numero_pedido} - {self.cliente_nombre}"

    def save(self, *args, **kwargs):
        """Genera número de pedido automático"""
        if not self.numero_pedido:
            ultimo_pedido = Pedido.objects.all().order_by('-id').first()
            if ultimo_pedido and ultimo_pedido.numero_pedido:
                try:
                    ultimo_numero = int(ultimo_pedido.numero_pedido.split('-')[1])
                    nuevo_numero = ultimo_numero + 1
                except:
                    nuevo_numero = 1
            else:
                nuevo_numero = 1
            self.numero_pedido = f"PED-{nuevo_numero:05d}"
        super().save(*args, **kwargs)

    def calcular_totales(self):
        """Calcula subtotal, descuentos y total del pedido"""
        self.subtotal = sum(item.get_subtotal() for item in self.items.all())
        self.descuento_total = sum(item.get_descuento() for item in self.items.all())
        self.total = self.subtotal - self.descuento_total
        self.save()


class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='items'
    )

    menu = models.ForeignKey(
        Menu,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Menú'
    )

    nombre_temporal = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Nombre personalizado'
    )

    cantidad = models.PositiveIntegerField(default=1)

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    descuento_aplicado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )

    observaciones = models.TextField(blank=True, null=True)




    class Meta:
        verbose_name = "Item del Pedido"
        verbose_name_plural = "Items del Pedido"

    def __str__(self):
        return f"{self.menu.nombre} x{self.cantidad}"

    def get_subtotal(self):
        """Calcula subtotal sin descuento"""
        return self.precio_unitario * self.cantidad

    def get_descuento(self):
        """Calcula el monto del descuento"""
        return self.get_subtotal() * (self.descuento_aplicado / 100)

    def get_total(self):
        """Calcula el total con descuento"""
        return self.get_subtotal() - self.get_descuento()