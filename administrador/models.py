from django.db import models
class Administrador(models.Model):
    usuario = models.OneToOneField("usuario.Usuario", on_delete=models.CASCADE)
    nivel_prioridad = models.IntegerField()

    def __str__(self):
        return f"Admin {self.usuario.nombre}"
