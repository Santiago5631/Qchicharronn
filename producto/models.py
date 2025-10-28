from django.db import models


# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey('marca.Marca', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey('categoria.Categoria', on_delete=models.CASCADE)
    proveedor = models.ForeignKey('proveedor.Proveedor', on_delete=models.CASCADE)
    unidad = models.CharField(
        max_length=20,
        choices=[('kg', 'Kilogramos'),
                 ('L', 'Litros'),
                 ("ml", "Millitros"),
                 ('u', 'Unidades'),
                 ('g', 'Gramos')]
    )

    tipo_uso = models.CharField(
        max_length=20,
        choices=[('plato', 'Plato'), ('venta', 'Venta')],
    )

    stock = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0, )

    def reducir_stock(self, cantidad):

        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
        else:
            raise ValueError("No hay suficiente stock")

    def __str__(self):

        return f"{self.nombre} ({self.stock})"

