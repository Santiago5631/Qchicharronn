from django.db import models

# Create your models here.
class Nomina(models.Model):
    empleado = models.ForeignKey('empleado.Empleado', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.DecimalField(max_digits=10, decimal_places=2)
    admin = models.ForeignKey('administrador.Administrador', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.pago}"