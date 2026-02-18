from django.db import models

class Cliente(models.Model):

    TIPO_DOCUMENTO = (
        ('CC', 'Cédula'),
        ('NIT', 'NIT'),
        ('CE', 'Cédula extranjería'),
    )

    nombre = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO, blank=True, null=True)
    numero_documento = models.CharField(max_length=50, blank=True,unique=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    es_predeterminado = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.es_predeterminado:
            Cliente.objects.filter(es_predeterminado=True).update(es_predeterminado=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
