from django.db import models

class Unidad(models.Model):
    TIPO_CHOICES = [
        ('peso', 'Por Peso (kg, g, L, ml...)'),
        ('unidad', 'Por Unidad (piezas, cajas...)'),
    ]

    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='unidad',
        help_text='Define si esta unidad es por peso/volumen o por conteo'
    )

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"