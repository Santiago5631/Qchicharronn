from django.db import models

class Unidad(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True,  # 🔒 evita duplicados (ej. “kg” y “kg” dos veces)
    )
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"
        ordering = ['nombre']
