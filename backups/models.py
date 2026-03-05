from django.db import models


class RegistroBackup(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tamanio_kb     = models.PositiveIntegerField(default=0)
    drive_file_id  = models.CharField(max_length=255, blank=True)
    exitoso        = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Registro de Backup'
        verbose_name_plural = 'Registros de Backups'

    def __str__(self):
        return f"{self.nombre_archivo} — {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"

    @property
    def tamanio_legible(self):
        if self.tamanio_kb < 1024:
            return f"{self.tamanio_kb} KB"
        return f"{self.tamanio_kb / 1024:.1f} MB"