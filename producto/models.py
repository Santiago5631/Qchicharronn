from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey('marca.Marca', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey('categoria.Categoria', on_delete=models.CASCADE)
    proveedor = models.ForeignKey('proveedor.Proveedor', on_delete=models.CASCADE)
    unidad = models.ForeignKey('unidad.Unidad', on_delete=models.CASCADE, null=False, blank=False)
    tipo_uso = models.CharField(max_length=20, choices=[('plato', 'Plato'), ('venta', 'Venta')])
    stock = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)

    # 👇 Nuevo campo para dividir áreas
    area_preparacion = models.CharField(
        max_length=20,
        choices=[
            ('parrilla', 'Parrilla'),
            ('cocina', 'Cocina'),
        ],
        default='cocina'
    )
    disponible = models.BooleanField(default=True)

    def reducir_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
        else:
            raise ValueError("No hay suficiente stock")

    def __str__(self):
        return f"{self.nombre} ({self.stock})"
