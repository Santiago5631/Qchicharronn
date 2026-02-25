from django.db import models
from django.utils import timezone
from usuario.models import Usuario


class Nomina(models.Model):
    TIPO_PAGO_CHOICES = [
        ('hora', 'Por Hora'),
        ('dia', 'Por Día'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    # Relación con usuario (empleado)
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='nominas')

    # Tipo de pago
    tipo_pago = models.CharField(max_length=10, choices=TIPO_PAGO_CHOICES, default='dia')

    # Valor por hora o día
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor por hora o día")

    # Cantidad de horas o días trabajados
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, help_text="Horas o días trabajados")

    # Total calculado automáticamente
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # Fechas
    fecha_inicio = models.DateField(help_text="Fecha de inicio del período")
    fecha_fin = models.DateField(help_text="Fecha de fin del período")
    fecha_pago = models.DateField(default=timezone.now, help_text="Fecha de pago")

    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    # Observaciones
    observaciones = models.TextField(blank=True, null=True)

    # Auditoría
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='nominas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nómina"
        verbose_name_plural = "Nóminas"
        ordering = ['-fecha_pago', '-fecha_creacion']

    def save(self, *args, **kwargs):
        # Calcular el total automáticamente
        self.total = self.valor_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Nómina {self.empleado.nombre} - {self.fecha_inicio} a {self.fecha_fin} - ${self.total}"

    def get_nombre_empleado(self):
        return self.empleado.nombre or self.empleado.email

    def get_cedula_empleado(self):
        return self.empleado.cedula or "N/A"