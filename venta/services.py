from decimal import Decimal
from venta.models import Venta

def crear_venta_desde_pedido(pedido):
    """
    Crea una venta automáticamente cuando se crea un pedido
    """
    if hasattr(pedido, 'venta'):
        return pedido.venta  # ya existe

    return Venta.objects.create(
        pedido=pedido,
        cliente_nombre=pedido.cliente_nombre,
        tipo_pedido=pedido.tipo_pedido,
        mesa=pedido.mesa if pedido.tipo_pedido == 'mesa' else None,
        subtotal=Decimal('0.00'),
        descuento_total=Decimal('0.00'),
        total=Decimal('0.00'),
    )
def finalizar_venta_y_pedido(venta):
    venta.estado = 'pagado'
    venta.save()

    pedido = venta.pedido
    pedido.estado = 'terminado'
    pedido.save()

