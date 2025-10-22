from django.db import models

class Empleado(models.Model):
    usuario = models.OneToOneField("usuario.Usuario", on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')]
    )

    def __str__(self):
        return f"{self.usuario.nombre}"