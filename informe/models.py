from django.db import models
class Informe(models.Model):
    TIPO_INFORME_CHOICES = [
        ('venta', 'Informe de Ventas'),
        ('compra', 'Informe de Compras'),
        ('nomina', 'Informe de Nómina'),
        ('personalizado', 'Otro'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_INFORME_CHOICES)
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    creado_por = models.ForeignKey('Administrador', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo}) - {self.fecha_inicio} a {self.fecha_fin}"
