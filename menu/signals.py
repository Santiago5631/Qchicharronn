from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Pedido, PedidoItem  # este es menu.Pedido


@receiver(post_save, sender=Pedido)  # menu.Pedido — para anular venta
def anular_venta_si_pedido_cancelado(sender, instance, **kwargs):
    if instance.estado == 'cancelado':
        if hasattr(instance, 'venta'):
            venta = instance.venta
            if venta.estado != 'anulada':
                venta.estado = 'anulada'
                venta.save()


def _serializar_pedido(pedido):
    items = []
    for item in pedido.items.select_related('menu__categoria_menu').all():
        if item.menu:
            items.append({
                'nombre': item.menu.nombre,
                'cantidad': item.cantidad,
                'categoria': item.menu.categoria_menu.nombre if item.menu.categoria_menu else None,
                'categoria_id': item.menu.categoria_menu.id if item.menu.categoria_menu else None,
                'observaciones': item.observaciones or '',
            })

    return {
        'numero_pedido': pedido.numero_pedido,
        'mesa': str(pedido.mesa) if pedido.mesa else 'Para llevar',
        'mesero': pedido.mesero.get_full_name() if pedido.mesero else 'Sin asignar',
        'estado': pedido.estado,
        'hora': pedido.fecha_creacion.strftime('%H:%M'),
        'items': items,
        'observaciones': pedido.observaciones or '',
    }


@receiver(post_save, sender=Pedido)  # 👈 cambiar string por el modelo directo
def pedido_guardado(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    pedido_data = _serializar_pedido(instance)

    for grupo in ['vista_parrilla', 'vista_cocina']:
        async_to_sync(channel_layer.group_send)(
            grupo,
            {
                'type': 'pedido_update',
                'pedido': pedido_data,
                'accion': 'nuevo' if created else 'actualizado',  # 👈 usar created directo
            }
        )