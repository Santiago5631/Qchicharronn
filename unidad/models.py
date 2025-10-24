from django.db import models

class Unidad(models.Model):
    class TipoUnidad(models.TextChoices):
        KILOGRAMO = 'kg', 'Kilogramos'
        LITRO = 'L', 'Litros'
        MILILITRO = "ml", "Millitros"
        UNIDAD = 'u', 'Unidades'
        GRAMO = 'g', 'Gramos'

    nombre = models.CharField(
        max_length=10,
        choices=TipoUnidad.choices,
        default=TipoUnidad.UNIDAD
    )
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # Muestra el nombre legible en el admin o en las vistas
        return self.get_nombre_display()
