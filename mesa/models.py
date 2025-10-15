from django.db import models

# Create your models here.
from django.db import models

class Mesa(models.Model):
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    numero = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Mesa {self.numero} - {self.ubicacion}"
