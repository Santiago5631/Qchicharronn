from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Producto


@receiver(pre_save, sender=Producto)
def asignar_tipo_inventario_automatico(sender, instance, **kwargs):
    """
    Asigna automáticamente el tipo_inventario según la unidad del producto.
    """
    print(f"🔍 SIGNAL EJECUTADO para: {instance.nombre}")

    if instance.unidad:
        print(f"   Unidad detectada: {instance.unidad.nombre}")

        # Unidades que se manejan por peso/volumen (convertir a minúsculas para comparar)
        unidades_peso = ['kg', 'g', 'l', 'ml']

        # Comparar en minúsculas para ignorar mayúsculas/minúsculas
        if instance.unidad.nombre.lower() in unidades_peso:
            instance.tipo_inventario = 'peso'
            print(f"   ✅ Asignado como PESO")
        else:
            instance.tipo_inventario = 'unidad'
            print(f"   ✅ Asignado como UNIDAD")
    else:
        print(f"   ⚠️ No tiene unidad asignada")