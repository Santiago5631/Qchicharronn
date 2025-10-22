from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    cargo = models.CharField(
        max_length=50,
        default="operador",
        choices=[
            ('mesero', 'Mesero'),
            ('administrador', 'Administrador'),
            ('cocinero', 'Cocinero'),
            ("proveedor", "Proveedor")
        ]
    )
    correo_electronico = models.EmailField()
    numero_celular = models.CharField(max_length=20)
    estado = models.CharField(
        max_length=20,
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')]
    )
    contraseña = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre