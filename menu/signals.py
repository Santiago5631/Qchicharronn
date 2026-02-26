from django.db.models.signals import post_save
from django.dispatch import receiver
from menu.models import Pedido


@receiver(post_save, sender=Pedido)
def anular_venta_si_pedido_cancelado(sender, instance, **kwargs):
    """
    Si el pedido pasa a estado 'cancelado',
    la venta asociada cambia a 'anulada'.
    """
    if instance.estado == 'cancelado':
        if hasattr(instance, 'venta'):
            venta = instance.venta
            if venta.estado != 'anulada':
                venta.estado = 'anulada'
                venta.save()
